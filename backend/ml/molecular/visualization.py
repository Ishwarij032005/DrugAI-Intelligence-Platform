"""
DrugAI — Molecule 2D structure visualization via RDKit (SVG output).
"""
from __future__ import annotations

from core.logging import get_logger

log = get_logger(__name__)

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    from rdkit.Chem.Draw import rdMolDraw2D
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

_SVG_STUB = """<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300">
  <rect width="300" height="300" fill="#0f172a"/>
  <text x="150" y="150" fill="#64748b" text-anchor="middle" font-size="14"
    font-family="monospace">RDKit not installed</text>
</svg>"""


def smiles_to_svg(smiles: str, width: int = 400, height: int = 300) -> str:
    """Convert SMILES to an SVG 2D structure diagram."""
    if not RDKIT_AVAILABLE:
        return _SVG_STUB

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return _SVG_STUB

    try:
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        drawer.drawOptions().addStereoAnnotation = True
        drawer.drawOptions().addAtomIndices = False

        # Dark background with blue atom colors
        drawer.drawOptions().backgroundColour = (0.06, 0.09, 0.16, 1.0)
        drawer.drawOptions().bondLineWidth = 2.0

        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        return drawer.GetDrawingText()
    except Exception as e:
        log.warning("svg_generation_failed", smiles=smiles[:30], error=str(e))
        return _SVG_STUB


def smiles_to_png_bytes(smiles: str, size: tuple[int, int] = (400, 300)) -> bytes | None:
    """Convert SMILES to PNG bytes (for embedding in reports)."""
    if not RDKIT_AVAILABLE:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    try:
        img = Draw.MolToImage(mol, size=size)
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception as e:
        log.warning("png_generation_failed", error=str(e))
        return None
