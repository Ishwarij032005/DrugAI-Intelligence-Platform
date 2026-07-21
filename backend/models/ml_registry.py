"""
DrugAI — ModelRegistry, TrainingJob, and Dataset models.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import AuditableModel, TimestampMixin, UUIDPrimaryKeyMixin
from core.database import Base


class ModelRegistry(AuditableModel):
    __tablename__ = "model_registry"

    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Classical | Boosted | Deep | Graph | Transformer | Ensemble

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # MLflow linkage
    mlflow_run_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    mlflow_experiment_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    artifact_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Deployment stage
    stage: Mapped[str] = mapped_column(String(50), default="staging", nullable=False, index=True)
    # staging | production | archived

    # Performance metrics (full dict for flexibility)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    # {accuracy, precision, recall, f1, roc_auc, latency_ms, ...}

    # Hyperparameters used
    params: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    # Feature info
    feature_names: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    target_columns: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    trained_on_dataset: Mapped[str | None] = mapped_column(String(200), nullable=True)

    def to_api_response(self) -> dict:
        """Returns shape matching frontend modelsApi.list() response."""
        m = self.metrics
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.model_type,
            "accuracy": m.get("accuracy", 0.0),
            "precision": m.get("precision", 0.0),
            "recall": m.get("recall", 0.0),
            "f1": m.get("f1", 0.0),
            "roc": m.get("roc_auc", 0.0),
            "latencyMs": m.get("latency_ms", 0),
            "stage": self.stage,
            "version": self.version,
        }


class TrainingJob(AuditableModel):
    __tablename__ = "training_jobs"

    experiment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True, index=True
    )
    model_name: Mapped[str] = mapped_column(String(200), nullable=False)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    # pending | running | completed | failed | cancelled

    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    current_epoch: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_epochs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    celery_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    metrics: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    logs: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    experiment: Mapped["Experiment | None"] = relationship("Experiment", back_populates="training_jobs")

    def duration_str(self) -> str:
        if not self.started_at or not self.completed_at:
            return "—"
        delta = self.completed_at - self.started_at
        h, m = divmod(int(delta.total_seconds() // 60), 60)
        return f"{h}h {m:02d}m" if h else f"{m}m"


class Dataset(AuditableModel):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Tox21 | ClinTox | SIDER | DrugBank | ChEMBL | local | uploaded

    version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    record_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    schema_: Mapped[dict] = mapped_column("schema", JSONB, default=dict, nullable=False)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=True, nullable=False)


# Forward reference
from models.project import Experiment  # noqa: E402
