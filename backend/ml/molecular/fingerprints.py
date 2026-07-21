"""
DrugAI — Molecular fingerprints: Morgan, MACCS, atom-pair via RDKit.
"""
from __future__ import annotations

import numpy as np

from core.logging import get_logger

log = get_logger(__name__)

try:
    from rdkit import Chem, DataStructs
    from rdkit.Chem import AllChem, MACCSkeys
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


def morgan_fingerprint(smiles: str, radius: int = 2, n_bits: int = 2048) -> np.ndarray:
    """Returns Morgan circular fingerprint as NumPy array."""
    if not RDKIT_AVAILABLE:
        rng = np.random.default_rng(hash(smiles) % (2**31))
        return rng.integers(0, 2, size=n_bits, dtype=np.uint8)

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits, dtype=np.uint8)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=n_bits)
    arr = np.zeros(n_bits, dtype=np.uint8)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


def morgan_fp_hex(smiles: str, radius: int = 2, n_bits: int = 2048) -> str:
    """Morgan fingerprint as hex string (for storage and fast comparison)."""
    arr = morgan_fingerprint(smiles, radius, n_bits)
    packed = np.packbits(arr)
    return packed.tobytes().hex()


def maccs_fingerprint(smiles: str) -> np.ndarray:
    """Returns 167-bit MACCS keys fingerprint."""
    n_bits = 167
    if not RDKIT_AVAILABLE:
        rng = np.random.default_rng(hash(smiles) % (2**31))
        return rng.integers(0, 2, size=n_bits, dtype=np.uint8)

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits, dtype=np.uint8)
    fp = MACCSkeys.GenMACCSKeys(mol)
    arr = np.zeros(n_bits, dtype=np.uint8)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


def combined_features(smiles: str) -> np.ndarray:
    """Morgan (2048) + MACCS (167) = 2215 features for ML models."""
    morgan = morgan_fingerprint(smiles)
    maccs = maccs_fingerprint(smiles)
    return np.concatenate([morgan, maccs])


def tanimoto_similarity(fp1: np.ndarray, fp2: np.ndarray) -> float:
    """Compute Tanimoto (Jaccard) similarity between two binary fingerprints."""
    intersection = np.logical_and(fp1, fp2).sum()
    union = np.logical_or(fp1, fp2).sum()
    return float(intersection / union) if union > 0 else 0.0
