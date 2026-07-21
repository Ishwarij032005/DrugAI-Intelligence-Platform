"""
DrugAI — Training orchestrator to train all models sequentially with MLflow logging.
Calculates and logs scientific parameters, metrics, and plots (confusion matrices, ROC curves, PR curves, calibration, feature importance).
"""
from __future__ import annotations

import time
import mlflow
import numpy as np
import pandas as pd
from pathlib import Path

from core.config import settings
from core.logging import get_logger
from ml.models.base_model import model_manager
from ml.data.dataset_loader import get_merged_dataset
from ml.data.feature_engineering import DESCRIPTOR_COLS, scale_features, load_scaler
from ml.data.protein_features import PROTEIN_FEATURE_DIM, resolve_target, get_protein_vector
from ml.evaluation import (
    save_and_log_plots, save_and_log_regression_plots, save_and_log_feature_importance
)

# Import models to ensure they are registered
import ml.models.toxicity.model
import ml.models.admet.model
import ml.models.dti.model
import ml.models.side_effects.model
import ml.models.similarity.model
import ml.models.recommendation.model

log = get_logger(__name__)

def train_all():
    start_time = time.perf_counter()
    log.info("training_all_models_started")
    
    # Configure MLflow tracking
    try:
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        log.info("mlflow_tracking_configured", uri=settings.mlflow_tracking_uri)
    except Exception as e:
        log.warning("mlflow_tracking_config_failed", error=str(e))
        
    df_test = get_merged_dataset("test")
    scaler = load_scaler()
    X_test_scaled = scale_features(df_test[DESCRIPTOR_COLS].values, scaler) if scaler else df_test[DESCRIPTOR_COLS].values

    # 1. Toxicity Ensemble
    log.info("training_toxicity_ensemble")
    tox_pred = model_manager.get("toxicity_ensemble")
    if tox_pred:
        mlflow.set_experiment("drugai_toxicity")
        with mlflow.start_run(run_name="toxicity_train"):
            tox_pred.train_and_save()
            metrics = tox_pred.get_metrics()
            mlflow.log_params({
                "model_type": tox_pred.model_type,
                "version": tox_pred.model_version,
                "estimators": 50,
                "max_depth": 4,
            })
            mlflow.log_metrics(metrics)
            
            # Generate test plots using the primary classifier (Hepatotoxicity)
            y_test_binary = (df_test["toxicity_risk"].str.lower().fillna("low").isin(["medium", "high"])).astype(int).values
            hep_model = tox_pred._models.get("Hepatotoxicity")
            if hep_model:
                probs = hep_model.predict_proba(X_test_scaled)[:, 1]
                save_and_log_plots(y_test_binary, probs, "Toxicity")
                save_and_log_feature_importance(hep_model.feature_importances_, DESCRIPTOR_COLS, "Toxicity")
                
            log.info("toxicity_ensemble_training_done", metrics=metrics)

    # 2. ADMET Profiler
    log.info("training_admet_profiler")
    admet_pred = model_manager.get("admet_profiler")
    if admet_pred:
        mlflow.set_experiment("drugai_admet")
        with mlflow.start_run(run_name="admet_train"):
            admet_pred.train_and_save()
            metrics = admet_pred.get_metrics()
            mlflow.log_params({
                "model_type": admet_pred.model_type,
                "version": admet_pred.model_version,
                "estimators": 50,
                "max_depth": 6,
            })
            mlflow.log_metrics(metrics)
            
            # Generate test plots for Absorption regressor
            abs_model = admet_pred._models.get("Absorption")
            if abs_model:
                y_test_abs = admet_pred._generate_admet_targets(df_test, "Absorption")
                preds_abs = abs_model.predict(X_test_scaled)
                save_and_log_regression_plots(y_test_abs, preds_abs, "ADMET_Absorption")
                save_and_log_feature_importance(abs_model.feature_importances_, DESCRIPTOR_COLS, "ADMET_Absorption")
                
            log.info("admet_profiler_training_done", metrics=metrics)

    # 3. Drug-Target Interaction Regressor
    log.info("training_dti_gcn")
    dti_pred = model_manager.get("dti_gcn")
    if dti_pred:
        mlflow.set_experiment("drugai_dti")
        with mlflow.start_run(run_name="dti_train"):
            dti_pred.train_and_save()
            metrics = dti_pred.get_metrics()
            mlflow.log_params({
                "model_type": dti_pred.model_type,
                "version": dti_pred.model_version,
                "estimators": 100,
                "max_depth": 5,
            })
            mlflow.log_metrics(metrics)
            
            # Generate test plots
            X_test_joint = dti_pred._build_joint_features(df_test, scaler)
            y_test_bind = df_test["binding_probability"].fillna(0.1).values
            preds_bind = dti_pred._model_xgb.predict(X_test_joint)
            
            save_and_log_regression_plots(y_test_bind, preds_bind, "DTI")
            feature_names = DESCRIPTOR_COLS + [f"protein_dim_{i}" for i in range(PROTEIN_FEATURE_DIM)]
            save_and_log_feature_importance(dti_pred._model_xgb.feature_importances_, feature_names, "DTI")
            
            log.info("dti_gcn_training_done", metrics=metrics)

    # 4. Side Effects Predictor
    log.info("training_side_effects_xgb")
    se_pred = model_manager.get("side_effects_xgb")
    if se_pred:
        mlflow.set_experiment("drugai_side_effects")
        with mlflow.start_run(run_name="side_effects_train"):
            se_pred.train_and_save()
            metrics = se_pred.get_metrics()
            mlflow.log_params({
                "model_type": se_pred.model_type,
                "version": se_pred.model_version,
                "estimators": 50,
                "max_depth": 4,
            })
            mlflow.log_metrics(metrics)
            
            # Plot metrics using the main side effect (Nausea)
            nausea_model = se_pred._models.get("Nausea")
            if nausea_model:
                y_test_nausea = se_pred._extract_labels(df_test, "Nausea")
                probs_nausea = nausea_model.predict_proba(X_test_scaled)[:, 1]
                save_and_log_plots(y_test_nausea, probs_nausea, "Side_Effects_Nausea")
                save_and_log_feature_importance(nausea_model.feature_importances_, DESCRIPTOR_COLS, "Side_Effects_Nausea")
                
            log.info("side_effects_xgb_training_done", metrics=metrics)

    elapsed = round(time.perf_counter() - start_time, 2)
    log.info("training_all_models_completed", total_time_sec=elapsed)
    print(f"Training successfully completed in {elapsed} seconds.")

if __name__ == "__main__":
    train_all()
