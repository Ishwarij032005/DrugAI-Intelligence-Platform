"""
DrugAI — Molecules router: validate, properties, SVG structure, similarity search.
"""
from __future__ import annotations

from fastapi import APIRouter, Path, Query
from fastapi.responses import Response

from auth.dependencies import OptionalUser
from core.exceptions import InvalidSMILESError
from ml.molecular.processor import validate_smiles, compute_properties
from ml.molecular.visualization import smiles_to_svg
from ml.models.base_model import model_manager

router = APIRouter(prefix="/molecules", tags=["Molecules"])


@router.post("/validate")
async def validate_molecule(body: dict, user: OptionalUser):
    """Validate SMILES and return canonical form + basic properties."""
    smiles = body.get("smiles", "").strip()
    if not smiles:
        raise InvalidSMILESError("SMILES is required.")
    canonical = validate_smiles(smiles)
    props = compute_properties(canonical)
    return {
        "valid": True,
        "canonical": canonical,
        "molecularWeight": props.mol_weight,
        "logP": props.logp,
        "tpsa": props.tpsa,
    }


@router.get("/{smiles}/properties")
async def molecule_properties(smiles: str, user: OptionalUser):
    """Full physicochemical property profile for a SMILES string."""
    import urllib.parse
    decoded = urllib.parse.unquote(smiles)
    props = compute_properties(decoded)
    return props.to_dict()


@router.get("/{smiles}/structure.svg", response_class=Response)
async def molecule_svg(
    smiles: str,
    user: OptionalUser,
    width: int = Query(400),
    height: int = Query(300),
):
    """Return 2D SVG structure of the molecule."""
    import urllib.parse
    decoded = urllib.parse.unquote(smiles)
    svg = smiles_to_svg(decoded, width=width, height=height)
    return Response(content=svg, media_type="image/svg+xml")


@router.post("/similarity")
async def similarity_search(body: dict, user: OptionalUser):
    """Find structurally similar compounds using Tanimoto fingerprint search."""
    query = body.get("query", body.get("smiles", "")).strip()
    top_k = body.get("topK", body.get("top_k", 10))

    if not query:
        raise InvalidSMILESError("Query SMILES is required.")

    searcher = model_manager.get("similarity_search")
    result = searcher.predict(query, top_k=top_k) if searcher else {"results": []}
    return result["results"]
