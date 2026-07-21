"""
DrugAI — Prediction and PredictionHistory models.
"""
from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import AuditableModel, TimestampMixin, UUIDPrimaryKeyMixin
from core.database import Base


class Prediction(AuditableModel):
    __tablename__ = "predictions"
    __table_args__ = (
        Index("ix_predictions_user_type", "user_id", "prediction_type"),
        Index("ix_predictions_status", "status"),
        Index("ix_predictions_created", "created_at"),
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    molecule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drug_molecules.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Input
    input_smiles: Mapped[str] = mapped_column(Text, nullable=False)
    drug_name: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    prediction_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # toxicity | admet | dti | side_effects | similarity | recommendation

    # Model info
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Result (full JSON blob — structure varies by type)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="success", nullable=False)
    # status: success | warning | danger | processing | failed

    # Performance
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # SHAP/LIME explanations (stored lazily)
    explanation: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Convenience top-level fields (redundant with result but queryable)
    toxicity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Relationships
    user: Mapped["User | None"] = relationship("User", back_populates="predictions")
    molecule: Mapped["DrugMolecule | None"] = relationship("DrugMolecule", back_populates="predictions")
    history: Mapped[list["PredictionHistory"]] = relationship(
        "PredictionHistory", back_populates="prediction", cascade="all, delete-orphan"
    )

    def to_list_item(self) -> dict:
        """Returns the shape expected by drugsApi.listPredictions() on the frontend."""
        return {
            "id": f"PRD-{str(self.id)[:8].upper()}",
            "drug": self.drug_name or "Unknown",
            "smiles": self.input_smiles,
            "toxicity": round(self.toxicity_score or 0),
            "confidence": round(self.confidence_score or 0),
            "model": self.model_used,
            "status": self.status,
            "createdAt": self.created_at.isoformat(),
        }


class PredictionHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "prediction_history"

    prediction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # created | exported | deleted | re-run
    snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)

    prediction: Mapped["Prediction"] = relationship("Prediction", back_populates="history")


# Forward references
from models.user import User  # noqa: E402
from models.molecule import DrugMolecule  # noqa: E402
