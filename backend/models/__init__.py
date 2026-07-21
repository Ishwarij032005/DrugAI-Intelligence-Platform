"""
DrugAI — Models package.
Import all models here so SQLAlchemy can register them with the metadata.
"""
from models.base import Base, AuditableModel  # noqa: F401
from models.user import Organization, Role, User, APIKey, Workspace  # noqa: F401
from models.molecule import DrugMolecule, ProteinSequence  # noqa: F401
from models.prediction import Prediction, PredictionHistory  # noqa: F401
from models.project import Project, Experiment  # noqa: F401
from models.ml_registry import ModelRegistry, TrainingJob, Dataset  # noqa: F401
from models.report import Report, Notification, AuditLog, SystemMetric, Feedback, SavedSearch  # noqa: F401

__all__ = [
    "Base",
    "AuditableModel",
    "Organization",
    "Role",
    "User",
    "APIKey",
    "Workspace",
    "DrugMolecule",
    "ProteinSequence",
    "Prediction",
    "PredictionHistory",
    "Project",
    "Experiment",
    "ModelRegistry",
    "TrainingJob",
    "Dataset",
    "Report",
    "Notification",
    "AuditLog",
    "SystemMetric",
    "Feedback",
    "SavedSearch",
]
