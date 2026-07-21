"""
DrugAI — Drug Molecule and Protein Sequence models.
"""
from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import AuditableModel


class DrugMolecule(AuditableModel):
    __tablename__ = "drug_molecules"
    __table_args__ = (
        Index("ix_molecules_inchikey", "inchikey"),
        UniqueConstraint("inchikey", name="uq_molecules_inchikey"),
    )

    # Identity
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    smiles: Mapped[str] = mapped_column(Text, nullable=False)
    canonical_smiles: Mapped[str | None] = mapped_column(Text, nullable=True)
    inchi: Mapped[str | None] = mapped_column(Text, nullable=True)
    inchikey: Mapped[str | None] = mapped_column(String(27), nullable=True)

    # Physicochemical properties (computed by RDKit)
    mol_weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    logp: Mapped[float | None] = mapped_column(Float, nullable=True)
    tpsa: Mapped[float | None] = mapped_column(Float, nullable=True)
    h_bond_donors: Mapped[int | None] = mapped_column(Integer, nullable=True)
    h_bond_acceptors: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rotatable_bonds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ring_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    heavy_atom_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    aromatic_rings: Mapped[int | None] = mapped_column(Integer, nullable=True)
    qed_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    sa_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Classification
    drug_class: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    atc_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)  # ChEMBL, PubChem, etc.

    # All RDKit descriptors stored as JSONB for flexibility
    descriptors: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    # Morgan fingerprint (stored as hex string for similarity search)
    morgan_fp_hex: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="molecule")


class ProteinSequence(AuditableModel):
    __tablename__ = "protein_sequences"
    __table_args__ = (
        UniqueConstraint("uniprot_id", name="uq_proteins_uniprot"),
    )

    uniprot_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    gene_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    organism: Mapped[str | None] = mapped_column(String(200), nullable=True)
    sequence: Mapped[str | None] = mapped_column(Text, nullable=True)
    length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_class: Mapped[str | None] = mapped_column(String(200), nullable=True)
    features: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


# Forward reference
from models.prediction import Prediction  # noqa: E402
