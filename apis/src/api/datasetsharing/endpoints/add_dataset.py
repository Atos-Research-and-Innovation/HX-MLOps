from src.api.datasetsharing.schemas.health import HealthResponse, HealthStatus
from src.api.datasetsharing.schemas.addDataset import Dataset, DatasetResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.datasetsharing.database import actions as db_actions

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, APIRouter, Form

import json

router = APIRouter()

@router.post(
    "/dataset",
    tags=["dataset"],
    summary="Add a new dataset with metainfo",
    description="Add a new dataset with meta information",
    response_model=DatasetResponse,
    responses={
        200: {
            "description": "Succesful operation",
            "content": {
                "application/json": {
                    "example": {
                        "name": "ispm_dataset",
                        "version": "1.0.0",
                        "dataType": "mixed",
                        "tag": "timeseries",
                        "parameters": {
                            "size": "350MB",
                            "columns": "date/node_1/node_2/node_3",
                            "row_number": "5000",
                        },
                    }
                }
            }
        },
        400: {
            "description": "Bad Request"
        },
        403: {
            "description": "Forbidden Request"
        },
        404: {
            "description": "Service status not found"
        }
    }
)
async def add_model(
    name: str = Form(...),
    version: str = Form(...),
    dataType: str = Form(...),
    tag: str = Form(...),
    parameters: str = Form(...),
    dataModelFile: UploadFile = File(...),
    datasetFile: UploadFile = File(...),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session)
):
    try:

        parameters = json.loads(parameters)
        
        dataset_data = Dataset(
            name=name,
            version=version,
            dataType=dataType,
            tag=tag,
            parameters=parameters,
        )

        logger.info(f"Adding dataset: {dataset_data.name}, version: {dataset_data.version}")

        try:
            dataModel_path = await minio_operations.upload_file_to_minio(dataModelFile, minio_session, minio_operations.BUCKET_REGISTRY)
            dataset_path = await minio_operations.upload_file_to_minio(datasetFile, minio_session, minio_operations.BUCKET_REGISTRY)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

        dataset_id = db_actions.save_dataset(dataset_data=dataset_data, dataset_path=dataset_path, dataModel_path=dataModel_path, db_session=db_session)

        return DatasetResponse(
            datasetIdentifier=dataset_id,
            name=dataset_data.name,
            version=dataset_data.version,
            dataType=dataset_data.dataType,
            tag=dataset_data.tag,
            parameters=dataset_data.parameters,
        )

    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")

    except Exception as e:
        logger.error(f"Error adding model: {e}")
        raise HTTPException(status_code=400, detail="Error adding dataset")