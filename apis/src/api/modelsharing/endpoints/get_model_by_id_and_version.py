from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
import os
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.modelsharing.database import actions as db_actions

router = APIRouter()

@router.get(
    "/model/by_id/{model_id}",
    tags=["model"],
    summary="Get model by ID and version",
    description="Service to get a model by model ID and version (default value 'latest')",
    response_description="Model file",
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"},
                    "example": "model_version.pkl",
                }
            },
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "Model not found"},
    },
)
async def get_model(
    model_id: str,
    version: str = Query("latest", description="Model version"),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session)
):
    try:
        model_data = db_actions.get_model_by_id_and_version(model_id, version, db_session)

        file_path = model_data.filePath 
        file = minio_operations.get_file_from_minio(file_path, minio_session)
        return StreamingResponse(file, media_type="application/octet-stream")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")