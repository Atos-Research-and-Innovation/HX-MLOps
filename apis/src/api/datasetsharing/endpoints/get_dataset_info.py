from src.api.datasetsharing.schemas.addDataset import DatasetResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.datasetsharing.database import actions as db_actions
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session


router = APIRouter()



@router.get(
    "/dataset/{dataset_id}/data",
    response_model=DatasetResponse,
    summary="getDatasetInfo",
    description="Service to get a dataset by dataset Id",
    tags=["dataset"]
)
async def get_dataset_info(
    dataset_id: str,
    version: str = Query("latest", description="dataset version"),
    db_session=Depends(db_operations.get_session)
):
    try:
        dataset_data = db_actions.get_dataset_by_id_and_version(dataset_id=dataset_id, version=version, db_session=db_session)

        return DatasetResponse(
            datasetIdentifier=dataset_id,
            name=dataset_data.name,
            version=dataset_data.version,
            dataType=dataset_data.dataType,
            tag=dataset_data.tag,
            parameters=dataset_data.parameters,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")