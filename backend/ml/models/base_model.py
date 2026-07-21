"""
DrugAI — ML model base class and model registry manager.
"""
from __future__ import annotations

import os
import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np

from core.config import settings
from core.logging import get_logger

log = get_logger(__name__)


class BasePredictor(ABC):
    """Abstract base for all DrugAI predictors."""

    model_name: str = "base"
    model_version: str = "1.0"
    model_type: str = "classical"

    def __init__(self):
        self._model: Any = None
        self._is_loaded: bool = False
        self._model_path: Path = settings.models_path / f"{self.model_name}.pkl"

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def save(self, path: Path | None = None) -> Path:
        """Serialize model to disk."""
        p = path or self._model_path
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "wb") as f:
            pickle.dump(self._model, f, protocol=pickle.HIGHEST_PROTOCOL)
        log.info("model_saved", name=self.model_name, path=str(p))
        return p

    def load(self, path: Path | None = None) -> bool:
        """Deserialize model from disk. Returns True if successful."""
        p = path or self._model_path
        if not p.exists():
            log.warning("model_not_found", name=self.model_name, path=str(p))
            return False
        try:
            with open(p, "rb") as f:
                self._model = pickle.load(f)
            self._is_loaded = True
            log.info("model_loaded", name=self.model_name, path=str(p))
            return True
        except Exception as e:
            log.error("model_load_failed", name=self.model_name, error=str(e))
            return False

    @abstractmethod
    def predict(self, smiles: str, **kwargs) -> dict[str, Any]:
        """Run prediction for a single molecule. Returns result dict."""
        ...

    @abstractmethod
    def get_metrics(self) -> dict[str, float]:
        """Return evaluation metrics for this model."""
        ...

    def _smiles_to_features(self, smiles: str) -> np.ndarray:
        """Default feature extraction: Morgan + MACCS fingerprints."""
        from ml.molecular.fingerprints import combined_features
        return combined_features(smiles)


# ── Global Model Registry (in-memory singleton) ─────────────────────────────────

class ModelManager:
    """Singleton that holds all loaded predictor instances."""

    _instance: "ModelManager | None" = None
    _predictors: dict[str, BasePredictor]

    def __new__(cls) -> "ModelManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._predictors = {}
        return cls._instance

    def register(self, predictor: BasePredictor) -> None:
        self._predictors[predictor.model_name] = predictor
        log.info("predictor_registered", name=predictor.model_name)

    def get(self, name: str) -> BasePredictor | None:
        return self._predictors.get(name)

    def load_all(self) -> dict[str, bool]:
        """Attempt to load all registered predictors. Returns {name: success}."""
        results: dict[str, bool] = {}
        for name, pred in self._predictors.items():
            if not pred.is_loaded:
                results[name] = pred.load()
            else:
                results[name] = True
        return results

    def list_loaded(self) -> list[str]:
        return [n for n, p in self._predictors.items() if p.is_loaded]


model_manager = ModelManager()
