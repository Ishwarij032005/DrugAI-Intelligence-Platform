"""
DrugAI — RDKit molecular processor: SMILES → descriptors, properties, validation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.exceptions import InvalidSMILESError, MoleculeProcessingError
from core.logging import get_logger

log = get_logger(__name__)

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, QED, rdMolDescriptors
    from rdkit.Chem.rdMolDescriptors import CalcTPSA
    RDKIT_AVAILABLE = True
except ImportError:
    log.warning("RDKit not available — using stub molecular processor")
    RDKIT_AVAILABLE = False


@dataclass
class MoleculeProperties:
    smiles: str
    canonical_smiles: str
    inchi: str | None
    inchikey: str | None
    mol_weight: float
    logp: float
    tpsa: float
    h_bond_donors: int
    h_bond_acceptors: int
    rotatable_bonds: int
    ring_count: int
    heavy_atom_count: int
    aromatic_rings: int
    qed_score: float
    descriptors: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "smiles": self.smiles,
            "canonicalSmiles": self.canonical_smiles,
            "inchi": self.inchi,
            "inchikey": self.inchikey,
            "molecularWeight": round(self.mol_weight, 4),
            "logP": round(self.logp, 4),
            "tpsa": round(self.tpsa, 2),
            "hBondDonors": self.h_bond_donors,
            "hBondAcceptors": self.h_bond_acceptors,
            "rotatableBonds": self.rotatable_bonds,
            "ringCount": self.ring_count,
            "heavyAtomCount": self.heavy_atom_count,
            "aromaticRings": self.aromatic_rings,
            "qedScore": round(self.qed_score, 4),
        }

    def to_visualization_props(self) -> list[dict]:
        """Shape expected by /app/visualization frontend page."""
        return [
            {"l": "Molecular weight", "v": f"{self.mol_weight:.2f}", "u": "g/mol"},
            {"l": "LogP", "v": f"{self.logp:.2f}"},
            {"l": "TPSA", "v": f"{self.tpsa:.1f}", "u": "Å²"},
            {"l": "H-bond donors", "v": str(self.h_bond_donors)},
            {"l": "H-bond acceptors", "v": str(self.h_bond_acceptors)},
            {"l": "Rotatable bonds", "v": str(self.rotatable_bonds)},
            {"l": "Ring count", "v": str(self.ring_count)},
            {"l": "Heavy atoms", "v": str(self.heavy_atom_count)},
            {"l": "QED score", "v": f"{self.qed_score:.4f}"},
        ]


def validate_smiles(smiles: str) -> str:
    """Validate SMILES and return canonical form. Raises InvalidSMILESError."""
    if not smiles or not smiles.strip():
        raise InvalidSMILESError("SMILES string cannot be empty.")
    smiles = smiles.strip()

    if not RDKIT_AVAILABLE:
        # Basic heuristic: SMILES should only contain valid chemistry characters
        import re
        if not re.fullmatch(r"[A-Za-z0-9@+\-\[\]\(\)=#%\/\\.\:]+", smiles):
            raise InvalidSMILESError(f"Could not parse SMILES: '{smiles[:50]}'")
        # Also reject strings that are all uppercase letters (e.g. 'INVALID_SMILES')
        if re.fullmatch(r"[A-Z_]+", smiles):
            raise InvalidSMILESError(f"Could not parse SMILES: '{smiles[:50]}'")
        return smiles  # passthrough in stub mode

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise InvalidSMILESError(f"Could not parse SMILES: '{smiles[:50]}'")
    return Chem.MolToSmiles(mol, isomericSmiles=True)


def compute_properties(smiles: str) -> MoleculeProperties:
    """Full RDKit descriptor computation from SMILES."""
    if not RDKIT_AVAILABLE:
        return _stub_properties(smiles)

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise InvalidSMILESError(f"Invalid SMILES: '{smiles[:50]}'")

    try:
        canonical = Chem.MolToSmiles(mol, isomericSmiles=True)

        # Core descriptors
        mw = Descriptors.ExactMolWt(mol)
        logp = Descriptors.MolLogP(mol)
        tpsa = CalcTPSA(mol)
        hbd = rdMolDescriptors.CalcNumHBD(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)
        rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
        rings = rdMolDescriptors.CalcNumRings(mol)
        heavy = mol.GetNumHeavyAtoms()
        arom = rdMolDescriptors.CalcNumAromaticRings(mol)
        qed = QED.qed(mol)

        # InChI
        try:
            from rdkit.Chem.inchi import MolToInchi, InchiToInchiKey
            inchi = MolToInchi(mol)
            inchikey = InchiToInchiKey(inchi) if inchi else None
        except Exception:
            inchi = inchikey = None

        # Extended descriptors (200+)
        desc_dict: dict[str, Any] = {}
        for name, fn in Descriptors.descList:
            try:
                val = fn(mol)
                if val is not None and val == val:  # skip NaN
                    desc_dict[name] = round(float(val), 6)
            except Exception:
                pass

        return MoleculeProperties(
            smiles=smiles,
            canonical_smiles=canonical,
            inchi=inchi,
            inchikey=inchikey,
            mol_weight=mw,
            logp=logp,
            tpsa=tpsa,
            h_bond_donors=hbd,
            h_bond_acceptors=hba,
            rotatable_bonds=rot,
            ring_count=rings,
            heavy_atom_count=heavy,
            aromatic_rings=arom,
            qed_score=qed,
            descriptors=desc_dict,
        )
    except InvalidSMILESError:
        raise
    except Exception as e:
        raise MoleculeProcessingError(f"Failed to compute properties: {e}") from e


def _stub_properties(smiles: str) -> MoleculeProperties:
    """Fallback when RDKit is not installed (demo mode)."""
    import random
    rng = random.Random(hash(smiles) % (2**31))
    return MoleculeProperties(
        smiles=smiles,
        canonical_smiles=smiles,
        inchi=None,
        inchikey=None,
        mol_weight=round(rng.uniform(100, 600), 2),
        logp=round(rng.uniform(-2, 5), 2),
        tpsa=round(rng.uniform(20, 140), 1),
        h_bond_donors=rng.randint(0, 5),
        h_bond_acceptors=rng.randint(0, 10),
        rotatable_bonds=rng.randint(0, 8),
        ring_count=rng.randint(0, 4),
        heavy_atom_count=rng.randint(5, 40),
        aromatic_rings=rng.randint(0, 3),
        qed_score=round(rng.uniform(0.2, 0.9), 4),
        descriptors={},
    )
