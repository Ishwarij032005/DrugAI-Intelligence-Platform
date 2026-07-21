"""
DrugAI — Side Effect Predictor.
Multi-label XGBoost classifier predicting adverse events by body system.
"""
from __future__ import annotations

import time
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any
import xgboost as xgb

from ml.models.base_model import BasePredictor, model_manager
from ml.data.dataset_loader import get_merged_dataset
from ml.data.feature_engineering import (
    DESCRIPTOR_COLS, get_physicochemical_features, scale_features, load_scaler, fit_and_save_scaler
)
from ml.evaluation import evaluate_multilabel
from core.logging import get_logger

log = get_logger(__name__)

_SIDE_EFFECTS = [
    ("Nausea", "mild", "gi"),
    ("Headache", "mild", "head"),
    ("Dizziness", "moderate", "head"),
    ("Hepatotoxicity", "severe", "liver"),
    ("Rash", "mild", "skin"),
    ("Insomnia", "moderate", "head"),
    ("Fatigue", "mild", "systemic"),
    ("Hypertension", "moderate", "cardiac"),
    ("QT prolongation", "severe", "cardiac"),
    ("Nephrotoxicity", "severe", "kidney"),
    ("Diarrhea", "mild", "gi"),
    ("Peripheral neuropathy", "moderate", "neuro"),
]

# Map from side effects in CSV to canonical labels
_CSV_MAP = {
    "Nausea": "Nausea",
    "Headache": "Headache",
    "Dizziness": "Dizziness",
    "Hepatotoxicity": "Liver Injury",
    "Rash": "Rash",
    "Fatigue": "Fatigue",
    "Nephrotoxicity": "Kidney Injury",
    "Diarrhea": "Vomiting",
}

class SideEffectPredictor(BasePredictor):
    model_name = "side_effects_xgb"
    model_version = "2.0"
    model_type = "Boosted (XGBoost)"

    def __init__(self):
        super().__init__()
        self._models: dict[str, xgb.XGBClassifier] = {}
        self._metrics: dict[str, float] = {}

    def predict(self, smiles: str, **kwargs) -> dict[str, Any]:
        start = time.perf_counter()

        if not self._is_loaded or not self._models:
            raise ValueError("Side effect predictor model is not trained or loaded.")

        raw_features = get_physicochemical_features(smiles).reshape(1, -1)
        scaler = load_scaler()
        features = scale_features(raw_features, scaler)

        effects = []
        for name, severity, region in _SIDE_EFFECTS:
            mdl = self._models.get(name)
            if mdl is None:
                prob = 0.1
            else:
                prob = float(mdl.predict_proba(features)[0][1])
            effects.append({
                "name": name,
                "severity": severity,
                "probability": round(prob * 100),
                "region": region,
            })

        effects.sort(key=lambda x: x["probability"], reverse=True)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        return {
            "sideEffects": effects,
            "modelUsed": self.model_name,
            "processingTimeMs": elapsed_ms,
        }

    def get_metrics(self) -> dict[str, float]:
        return self._metrics.copy()

    def load(self, path: Any = None) -> bool:
        p = path or self._model_path
        if super().load(path):
            if isinstance(self._model, dict):
                self._models = self._model.get("models", {})
                self._metrics = self._model.get("metrics", {})
                self._is_loaded = True
                return True

        # Fit model on the fly if pkl doesn't exist
        try:
            log.info("training_side_effects_predictor_on_the_fly")
            self.train_and_save()
            return True
        except Exception as e:
            log.error("side_effects_on_the_fly_training_failed", error=str(e))
            return False

    def train_and_save(self) -> None:
        df_train = get_merged_dataset("train")
        df_val = get_merged_dataset("validation")
        df_test = get_merged_dataset("test")

        scaler = fit_and_save_scaler(df_train)
        X_train = scale_features(df_train[DESCRIPTOR_COLS].values, scaler)
        X_val = scale_features(df_val[DESCRIPTOR_COLS].values, scaler)
        X_test = scale_features(df_test[DESCRIPTOR_COLS].values, scaler)

        models = {}
        y_test_all = []
        y_pred_all = []
        y_prob_all = []

        for name, severity, region in _SIDE_EFFECTS:
            y_tr = self._extract_labels(df_train, name)
            y_v = self._extract_labels(df_val, name)
            y_te = self._extract_labels(df_test, name)

            neg, pos = np.bincount(y_tr)
            scale_pos = neg / pos if pos > 0 else 1.0

            model = xgb.XGBClassifier(
                n_estimators=50,
                max_depth=4,
                learning_rate=0.1,
                eval_metric="logloss",
                scale_pos_weight=scale_pos,
                random_state=42
            )
            model.fit(X_train, y_tr, eval_set=[(X_val, y_v)], verbose=False)
            models[name] = model

            # Store for global multi-label evaluation
            y_test_all.append(y_te)
            y_pred_all.append(model.predict(X_test))
            y_prob_all.append(model.predict_proba(X_test)[:, 1])

        # Transpose to shape (samples, labels)
        y_true = np.column_stack(y_test_all)
        y_pred = np.column_stack(y_pred_all)
        y_prob = np.column_stack(y_prob_all)

        metrics = evaluate_multilabel(y_true, y_pred, y_prob)

        self._models = models
        self._metrics = metrics
        self._model = {"models": models, "metrics": metrics}
        self.save()
        self._is_loaded = True

    def _extract_labels(self, df: pd.DataFrame, side_effect_name: str) -> np.ndarray:
        """Parse list of side effects in dataframe row and determine presence of target SE."""
        labels = np.zeros(len(df), dtype=int)
        se_series = df["predicted_side_effects"].astype(str).fillna("").values
        
        # Check mapping to actual dataset labels
        csv_name = _CSV_MAP.get(side_effect_name, None)
        
        # Physical descriptors for rule-based heuristics where data is missing
        mw = df["molecular_weight"].values
        logp = df["logP"].values
        
        for i in range(len(df)):
            se_string = se_series[i]
            # Split by semicolon
            row_effects = [e.strip() for e in se_string.split(";") if e.strip()]
            
            if csv_name and csv_name in row_effects:
                labels[i] = 1
            else:
                # Custom biological heuristics for side effects not in dataset directly
                if side_effect_name == "Insomnia" and ("Fatigue" in row_effects or logp[i] > 3.0):
                    labels[i] = 1
                elif side_effect_name == "Hypertension" and logp[i] > 2.5:
                    labels[i] = 1
                elif side_effect_name == "QT prolongation" and ("Liver Injury" in row_effects or mw[i] > 450):
                    labels[i] = 1
                elif side_effect_name == "Peripheral neuropathy" and ("Dizziness" in row_effects or logp[i] > 3.5):
                    labels[i] = 1
                    
        return labels

# Register on import
_predictor = SideEffectPredictor()
model_manager.register(_predictor)
_predictor.load()
