"""
DrugAI — Project and Experiment models.
"""
from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import AuditableModel


class Project(AuditableModel):
    __tablename__ = "projects"

    workspace_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="SET NULL"), nullable=True, index=True
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)

    workspace: Mapped["Workspace | None"] = relationship("Workspace", back_populates="projects")
    experiments: Mapped[list["Experiment"]] = relationship("Experiment", back_populates="project")


class Experiment(AuditableModel):
    __tablename__ = "experiments"

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mlflow_experiment_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)

    project: Mapped["Project | None"] = relationship("Project", back_populates="experiments")
    training_jobs: Mapped[list["TrainingJob"]] = relationship("TrainingJob", back_populates="experiment")


# Forward references
from models.user import Workspace  # noqa: E402
from models.ml_registry import TrainingJob  # noqa: E402
