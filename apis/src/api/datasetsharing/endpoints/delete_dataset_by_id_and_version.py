from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.datasetsharing.database import actions as db_actions
from src.api.datasetsharing.schemas.addDataset import DatasetResponse
import os

router = APIRouter()

@router.delete(
    "/dataset/{dataset_id}",
    tags=["dataset"],
    summary="Delete dataset by ID and version",
    description="Service to delete a dataset and metainfo by dataset Id",
    operation_id="deleteDataset",
    response_model=DatasetResponse,
    responses={
        200: {
            "message": "Successful operation",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/DatasetResponse"
                    }
                }
            }
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "Dataset not found"},
    },
)
async def delete_model(
    dataset_id: str,
    version: str = Query(..., description="Version of the dataset in the catalogue"),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session),
):
    dataset_data = db_actions.get_dataset_by_id_and_version(dataset_id, version, db_session)

    try:
        db_actions.delete_dataset(dataset_id, version, db_session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting dataset from database: {str(e)}")

    try:
        dataset_path = dataset_data.datasetPath 
        dataModel_path = dataset_data.dataModelPath
        minio_operations.delete_object(minio_session, dataset_path) 
        minio_operations.delete_object(minio_session, dataModel_path) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting dataset files: {str(e)}")

    return DatasetResponse(
            datasetIdentifier=dataset_id,
            name=dataset_data.name,
            version=dataset_data.version,
            dataType=dataset_data.dataType,
            tag=dataset_data.tag,
            parameters=dataset_data.parameters,
        )