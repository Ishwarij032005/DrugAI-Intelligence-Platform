"""
DrugAI — Drug-Target Interaction Predictor.
Uses drug descriptors and protein composition features for binding affinity regression.
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
from ml.data.protein_features import get_protein_vector, resolve_target
from ml.evaluation import evaluate_regression
from core.logging import get_logger

log = get_logger(__name__)

_KNOWN_TARGETS = [
    {"target": "BCR-ABL1", "uniprot": "P00519", "class": "Kinase"},
    {"target": "c-KIT", "uniprot": "P10721", "class": "Kinase"},
    {"target": "PDGFRα", "uniprot": "P16234", "class": "Kinase"},
    {"target": "c-SRC", "uniprot": "P12931", "class": "Kinase"},
    {"target": "EGFR", "uniprot": "P00533", "class": "Kinase"},
    {"target": "VEGFR2", "uniprot": "P35968", "class": "Kinase"},
    {"target": "CDK2", "uniprot": "P24941", "class": "Kinase"},
    {"target": "HER2", "uniprot": "P04626", "class": "Kinase"},
]

class DTIPredictor(BasePredictor):
    model_name = "dti_gcn"
    model_version = "2.0"
    model_type = "Boosted Regressor (XGBoost)"

    def __init__(self):
        super().__init__()
        self._model_xgb: xgb.XGBRegressor | None = None
        self._metrics: dict[str, float] = {}

    def predict(self, smiles: str, protein: str = "BCR-ABL1", **kwargs) -> dict[str, Any]:
        start = time.perf_counter()

        if not self._is_loaded or self._model_xgb is None:
            raise ValueError("DTI model is not trained or loaded.")

        # Extract & scale drug features
        raw_drug_feat = get_physicochemical_features(smiles).reshape(1, -1)
        scaler = load_scaler()
        drug_feat = scale_features(raw_drug_feat, scaler)[0]

        # Normalise request protein
        canonical_req_protein = resolve_target(protein)

        interactions = []
        # Run prediction for all known targets to fill the dropdown and list
        for idx, target_info in enumerate(_KNOWN_TARGETS):
            target_name = target_info["target"]
            norm_target_name = resolve_target(target_name)
            
            # Extract protein feature vector
            prot_feat = get_protein_vector(norm_target_name)
            
            # Combine drug and protein features (21-dim)
            x_input = np.concatenate([drug_feat, prot_feat]).reshape(1, -1)
            
            # Predict binding probability (0.0 to 1.0)
            prob = float(self._model_xgb.predict(x_input)[0])
            prob = max(0.0, min(1.0, prob))
            
            # Convert to Kd in nM: Kd = 10^(9 - 8 * prob)
            # e.g., prob = 1.0 -> Kd = 10 nM, prob = 0.0 -> Kd = 10^9 nM
            kd_nm = round(10 ** (9 - 8 * prob), 2)
            
            # Bound check for extremely large Kd
            if kd_nm > 1000000:
                kd_str = "> 1 mM"
            elif kd_nm > 1000:
                kd_str = f"{round(kd_nm / 1000, 2)} uM"
            else:
                kd_str = f"{kd_nm} nM"

            confidence = round(prob * 100)

            interactions.append({
                "target": target_name,
                "uniprot": target_info["uniprot"],
                "class": target_info["class"],
                "kd": kd_str,
                "kd_value": kd_nm,
                "confidence": confidence,
            })

        # Sort targets by affinity (lowest Kd first)
        interactions.sort(key=lambda x: x["kd_value"])
        primary = interactions[0]

        # Generate a heatmap grid based on actual feature importance
        # Use drug descriptors + protein features interaction values
        heatmap = []
        for i in range(len(_KNOWN_TARGETS)):
            t_name = resolve_target(_KNOWN_TARGETS[i]["target"])
            p_vec = get_protein_vector(t_name)
            row = []
            for j in range(12):
                # Pseudo heatmap mapping representation of drug-target compatibility
                val = abs(drug_feat[j % len(drug_feat)] * p_vec[j % len(p_vec)])
                row.append(round(float(val), 3))
            heatmap.append(row)

        elapsed_ms = int((time.perf_counter() - start) * 1000)

        return {
            "primaryTarget": primary["target"],
            "primaryKd": primary["kd"],
            "confidence": primary["confidence"],
            "interactions": interactions,
            "heatmap": heatmap,
            "modelUsed": self.model_name,
            "processingTimeMs": elapsed_ms,
        }

    def get_metrics(self) -> dict[str, float]:
        return self._metrics.copy()

    def load(self, path: Any = None) -> bool:
        p = path or self._model_path
        if super().load(path):
            if isinstance(self._model, dict):
                self._model_xgb = self._model.get("model", None)
                self._metrics = self._model.get("metrics", {})
                self._is_loaded = True
                return True

        # Fit model on the fly if pkl doesn't exist
        try:
            log.info("training_dti_model_on_the_fly")
            self.train_and_save()
            return True
        except Exception as e:
            log.error("dti_on_the_fly_training_failed", error=str(e))
            return False

    def train_and_save(self) -> None:
        df_train = get_merged_dataset("train")
        df_val = get_merged_dataset("validation")
        df_test = get_merged_dataset("test")

        scaler = fit_and_save_scaler(df_train)

        # Build feature matrices
        X_train = self._build_joint_features(df_train, scaler)
        X_val = self._build_joint_features(df_val, scaler)
        X_test = self._build_joint_features(df_test, scaler)

        y_train = df_train["binding_probability"].fillna(0.1).values
        y_val = df_val["binding_probability"].fillna(0.1).values
        y_test = df_test["binding_probability"].fillna(0.1).values

        model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

        preds = model.predict(X_test)
        metrics = evaluate_regression(y_test, preds)

        self._model_xgb = model
        self._metrics = metrics
        self._model = {"model": model, "metrics": metrics}
        self.save()
        self._is_loaded = True

    def _build_joint_features(self, df: pd.DataFrame, scaler: Any) -> np.ndarray:
        """Concatenate scaled drug features and protein target features for each row."""
        drug_feats = scale_features(df[DESCRIPTOR_COLS].values, scaler)
        
        target_names = df["target_protein"].astype(str).values
        prot_feats = []
        for name in target_names:
            resolved = resolve_target(name)
            prot_feats.append(get_protein_vector(resolved))
            
        prot_feats_arr = np.array(prot_feats, dtype=np.float32)
        return np.column_stack([drug_feats, prot_feats_arr])

# Register on import
_predictor = DTIPredictor()
model_manager.register(_predictor)
_predictor.load()
