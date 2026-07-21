"""
DrugAI — Evaluation and Plotting Helpers.
Calculates scientific metrics and logs plots/artifacts to MLflow.
"""
from __future__ import annotations

import os
import tempfile
import numpy as np
import pandas as pd
from typing import Any
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    precision_recall_curve, auc, mean_squared_error, mean_absolute_error, r2_score,
    confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
)
from sklearn.calibration import calibration_curve
import mlflow
from core.logging import get_logger

log = get_logger(__name__)

def evaluate_classification(
    y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray, prefix: str = ""
) -> dict[str, float]:
    """Calculate standard classification metrics."""
    metrics = {}
    metrics[f"{prefix}accuracy"] = float(accuracy_score(y_true, y_pred))
    # Handle multiclass or binary
    is_multiclass = len(np.unique(y_true)) > 2
    average = "macro" if is_multiclass else "binary"
    
    metrics[f"{prefix}precision"] = float(precision_score(y_true, y_pred, average=average, zero_division=0))
    metrics[f"{prefix}recall"] = float(recall_score(y_true, y_pred, average=average, zero_division=0))
    metrics[f"{prefix}f1"] = float(f1_score(y_true, y_pred, average=average, zero_division=0))
    
    try:
        if is_multiclass:
            # y_prob should be shape (n_samples, n_classes)
            metrics[f"{prefix}roc_auc"] = float(roc_auc_score(y_true, y_prob, multi_class="ovr", average="macro"))
        else:
            metrics[f"{prefix}roc_auc"] = float(roc_auc_score(y_true, y_prob))
            # PR-AUC
            precision, recall, _ = precision_recall_curve(y_true, y_prob)
            metrics[f"{prefix}pr_auc"] = float(auc(recall, precision))
    except Exception as e:
        log.warning("auc_calculation_failed", error=str(e))
        metrics[f"{prefix}roc_auc"] = 0.5
        if not is_multiclass:
            metrics[f"{prefix}pr_auc"] = 0.5
            
    return metrics

def evaluate_regression(
    y_true: np.ndarray, y_pred: np.ndarray, prefix: str = ""
) -> dict[str, float]:
    """Calculate standard regression metrics (ADMET, DTI binding affinity)."""
    metrics = {}
    metrics[f"{prefix}rmse"] = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    metrics[f"{prefix}mae"] = float(mean_absolute_error(y_true, y_pred))
    metrics[f"{prefix}r2"] = float(r2_score(y_true, y_pred))
    return metrics

def evaluate_multilabel(
    y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray, prefix: str = ""
) -> dict[str, float]:
    """Calculate multi-label classification metrics (Side Effects)."""
    from sklearn.metrics import hamming_loss
    metrics = {}
    metrics[f"{prefix}micro_f1"] = float(f1_score(y_true, y_pred, average="micro", zero_division=0))
    metrics[f"{prefix}macro_f1"] = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    metrics[f"{prefix}hamming_loss"] = float(hamming_loss(y_true, y_pred))
    return metrics

def save_and_log_plots(
    y_true: np.ndarray, y_prob: np.ndarray, model_name: str, is_multiclass: bool = False
):
    """Generate and log scientific plots to MLflow."""
    if is_multiclass or len(np.unique(y_true)) > 2:
        # Skip custom binary plots for multiclass
        return
        
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Confusion Matrix
        plt.figure()
        y_pred = (y_prob >= 0.5).astype(int)
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        cm_path = os.path.join(tmpdir, "confusion_matrix.png")
        plt.savefig(cm_path)
        plt.close()
        mlflow.log_artifact(cm_path)

        # 2. ROC Curve
        plt.figure()
        RocCurveDisplay.from_predictions(y_true, y_prob)
        roc_path = os.path.join(tmpdir, "roc_curve.png")
        plt.savefig(roc_path)
        plt.close()
        mlflow.log_artifact(roc_path)

        # 3. Precision-Recall Curve
        plt.figure()
        PrecisionRecallDisplay.from_predictions(y_true, y_prob)
        pr_path = os.path.join(tmpdir, "precision_recall_curve.png")
        plt.savefig(pr_path)
        plt.close()
        mlflow.log_artifact(pr_path)

        # 4. Calibration Curve
        plt.figure()
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
        plt.plot(prob_pred, prob_true, marker="o", label="Model")
        plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect Calibration")
        plt.xlabel("Predicted Probability")
        plt.ylabel("True Probability")
        plt.title("Calibration Curve")
        plt.legend()
        cal_path = os.path.join(tmpdir, "calibration_curve.png")
        plt.savefig(cal_path)
        plt.close()
        mlflow.log_artifact(cal_path)

def save_and_log_regression_plots(y_true: np.ndarray, y_pred: np.ndarray, model_name: str):
    """Generate and log regression scatter plots to MLflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        plt.figure()
        plt.scatter(y_true, y_pred, alpha=0.5)
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--")
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Predicted vs True - {model_name}")
        scatter_path = os.path.join(tmpdir, "predicted_vs_true.png")
        plt.savefig(scatter_path)
        plt.close()
        mlflow.log_artifact(scatter_path)

def save_and_log_feature_importance(importances: np.ndarray, feature_names: list[str], model_name: str):
    """Log feature importance plot to MLflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        plt.figure(figsize=(8, 6))
        indices = np.argsort(importances)
        plt.barh(range(len(indices)), importances[indices], align="center")
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel("Relative Importance")
        plt.title(f"Feature Importance - {model_name}")
        feat_path = os.path.join(tmpdir, "feature_importance.png")
        plt.savefig(feat_path, bbox_inches="tight")
        plt.close()
        mlflow.log_artifact(feat_path)
