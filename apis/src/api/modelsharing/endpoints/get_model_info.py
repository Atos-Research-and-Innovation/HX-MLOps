from src.api.modelsharing.schemas.addModel import ModelResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.modelsharing.database import actions as db_actions
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session


router = APIRouter()



@router.get(
    "/model/{model_id}/data",
    response_model=ModelResponse,
    summary="getModelInfo",
    description="Service to get a model by model Id",
    tags=["model"]
)
async def get_model_info(
    model_id: str,
    version: str = Query("latest", description="Model version"),
    db_session=Depends(db_operations.get_session)
):
    try:
        model_data = db_actions.get_model_by_id_and_version(model_id, version, db_session)

        return ModelResponse(
            modelIdentifier=model_data.id,
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

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")