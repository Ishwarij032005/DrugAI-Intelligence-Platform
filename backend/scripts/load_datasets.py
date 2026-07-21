"""
DrugAI — ETL script to load datasets from the local bundle into the database.
"""
import asyncio
import csv
from pathlib import Path

from core.config import settings
from core.database import get_db_context
from core.logging import get_logger
from ml.molecular.processor import validate_smiles, compute_properties
from models.molecule import DrugMolecule

log = get_logger(__name__)

async def load_datasets():
    log.info("starting_dataset_load", path=str(settings.datasets_path))
    
    if not settings.datasets_path.exists():
        log.warning("dataset_bundle_not_found", path=str(settings.datasets_path))
        return

    csv_path = settings.datasets_path / "drugs.csv"
    if not csv_path.exists():
        log.warning("drugs_csv_not_found", path=str(csv_path))
        return

    async with get_db_context() as db:
        # Simple import for demo purposes
        count = 0
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                smiles = row.get("smiles")
                if not smiles:
                    continue
                
                try:
                    props = compute_properties(smiles)
                    mol = DrugMolecule(
                        name=row.get("name", f"Compound-{count}"),
                        smiles=smiles,
                        canonical_smiles=props.canonical_smiles,
                        mol_weight=props.mol_weight,
                        logp=props.logp,
                        tpsa=props.tpsa,
                        source="synthetic_bundle",
                        descriptors=props.descriptors,
                    )
                    db.add(mol)
                    count += 1
                    
                    if count % 100 == 0:
                        await db.flush()
                        log.info("loaded_molecules", count=count)
                        
                except Exception as e:
                    log.debug("skip_molecule", smiles=smiles, error=str(e))
        
        await db.commit()
        log.info("dataset_load_complete", total_loaded=count)

if __name__ == "__main__":
    asyncio.run(load_datasets())
