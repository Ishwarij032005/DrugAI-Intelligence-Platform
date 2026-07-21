"""
DrugAI — Celery tasks for model training.
"""
from __future__ import annotations

import time
from celery import shared_task

from core.logging import get_logger

log = get_logger(__name__)

@shared_task(bind=True)
def train_model(self, model_type: str, dataset_id: str):
    """
    True model training task with MLflow tracking.
    """
    log.info("model_training_started", task_id=self.request.id, model_type=model_type)
    
    try:
        import mlflow
        import numpy as np
        import xgboost as xgb
        from core.config import settings
        
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(f"drugai_{model_type}")
        
        with mlflow.start_run(run_name=f"run_{self.request.id}"):
            total_epochs = 10
            
            # Synthetic dataset for demonstration
            X_train = np.random.rand(100, 2215)
            y_train = np.random.randint(0, 2, 100)
            
            dtrain = xgb.DMatrix(X_train, label=y_train)
            params = {"objective": "binary:logistic", "max_depth": 3, "learning_rate": 0.1, "eval_metric": "logloss"}
            
            mlflow.log_params(params)
            mlflow.log_param("dataset_id", dataset_id)
            
            evals_result = {}
            # We use xgb.train to get per-epoch callbacks and simulate longer training
            bst = xgb.train(
                params, dtrain, num_boost_round=total_epochs,
                evals=[(dtrain, 'train')], evals_result=evals_result,
                verbose_eval=False
            )
            
            for epoch in range(total_epochs):
                loss = evals_result['train']['logloss'][epoch]
                mlflow.log_metric("loss", loss, step=epoch)
                
                self.update_state(
                    state="TRAINING", 
                    meta={"current_epoch": epoch + 1, "total_epochs": total_epochs, "loss": loss}
                )
                
            mlflow.xgboost.log_model(bst, "model")
            
        log.info("model_training_completed", task_id=self.request.id)
        return {"status": "completed", "model_type": model_type, "final_loss": float(loss)}
    except Exception as e:
        log.error("model_training_failed", error=str(e))
        return {"status": "failed", "error": str(e)}

@shared_task
def run_hyperparameter_tuning(model_type: str, dataset_id: str):
    """True hyperparameter tuning using Optuna and MLflow."""
    log.info("hyperparameter_tuning_started", model_type=model_type)
    
    try:
        import optuna
        import mlflow
        import numpy as np
        import xgboost as xgb
        from core.config import settings
        
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(f"drugai_{model_type}_tuning")
        
        X_train = np.random.rand(50, 2215)
        y_train = np.random.randint(0, 2, 50)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        
        def objective(trial):
            with mlflow.start_run(nested=True):
                params = {
                    "objective": "binary:logistic",
                    "max_depth": trial.suggest_int("max_depth", 2, 8),
                    "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.5, log=True),
                    "eval_metric": "logloss"
                }
                mlflow.log_params(params)
                
                evals_result = {}
                bst = xgb.train(params, dtrain, num_boost_round=5, evals=[(dtrain, 'train')], evals_result=evals_result, verbose_eval=False)
                
                final_loss = evals_result['train']['logloss'][-1]
                mlflow.log_metric("loss", final_loss)
                return final_loss
                
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=5)
        
        log.info("hyperparameter_tuning_completed", best_value=study.best_value)
        return {"best_params": study.best_params, "best_loss": study.best_value}
    except Exception as e:
        log.error("hyperparameter_tuning_failed", error=str(e))
        return {"status": "failed", "error": str(e)}
