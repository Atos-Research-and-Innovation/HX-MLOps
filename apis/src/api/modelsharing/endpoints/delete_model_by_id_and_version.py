from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.modelsharing.database import actions as db_actions
from src.api.modelsharing.schemas.addModel import ModelResponse
import os

router = APIRouter()

@router.delete(
    "/model/{model_id}",
    tags=["model"],
    summary="Delete model by ID and version",
    description="Service to delete a model and metainfo by model Id",
    operation_id="deleteModel",
    response_model=ModelResponse,
    responses={
        200: {
            "message": "Successful operation",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ModelResponse"
                    }
                }
            }
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "Model not found"},
    },
)
async def delete_model(
    model_id: str,
    version: str = Query(..., description="Version of the model in the catalogue"),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session),
):
    model_data = db_actions.get_model_by_id_and_version(model_id, version, db_session)

    try:
        db_actions.delete_model(model_id, version, db_session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting model from database: {str(e)}")

    try:
        file_path = model_data.filePath 
        minio_operations.delete_object(minio_session, file_path) 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting model file: {str(e)}")

    return ModelResponse(
            modelIdentifier=model_id,
            name=model_data.name,
            version=model_data.version,
            status=model_data.status,
            library=model_data.library,
            libraryVersion=model_data.libraryVersion,
            domain=model_data.domain,
            tag=model_data.tag,
            parameters=model_data.parameters,
            characteristics=model_data.characteristics
        )