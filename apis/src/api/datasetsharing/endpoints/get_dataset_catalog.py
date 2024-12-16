from src.api.datasetsharing.schemas.addDataset import DatasetResponse
from src.api.datasetsharing.schemas.datasetCatalog import DatasetCatalogResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.datasetsharing.database import actions as db_actions
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session


router = APIRouter()

@router.get(
    "/dataset_catalog",
    tags=["dataset"],
    summary="Get dataset catalog by filters",
    description="Service to get a dataset catalog based on provided filters",
    operation_id="getDatasetCatalog",
    response_model=DatasetCatalogResponse,
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/DatasetCatalog"
                    }
                }
            }
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "Dataset not found"},
    },
)
async def get_dataset_catalog(
    tag: Optional[str] = Query(None, description="Filter models by tag"),
    dataType: Optional[str] = Query(None, description="Filter models by status", enum=["production", "synthetic", "mixed"]),
    name: Optional[str] = Query(None, description="Filter models by name"),
    version: Optional[str] = Query(None, description="Filter models by version"),
    db_session: Session = Depends(db_operations.get_session),
):
    datasets_data = db_actions.get_filtered_datasets(db_session, tag=tag, dataType=dataType, name=name, version=version)

    if not datasets_data:
        raise HTTPException(status_code=404, detail="No datasets found matching the filters")

    responses = []
    for dataset in datasets_data:
        datasetres = DatasetResponse(
            datasetIdentifier=dataset.id,
            name=dataset.name,
            version=dataset.version,
            dataType=dataset.dataType,
            tag=dataset.tag,
            parameters=dataset.parameters,
        )
        responses.append(datasetres)

    
    return DatasetCatalogResponse(datasets=responses)
