from src.api.modelsharing.schemas.health import HealthResponse, HealthStatus
from src.api.modelsharing.schemas.addModel import Model, ModelResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.modelsharing.database import actions as db_actions

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, APIRouter, Form

import json

router = APIRouter()

@router.post(
    "/model",
    tags=["model"],
    summary="Add a new model with metainfo",
    description="Add a new model with meta information",
    response_model=ModelResponse,
    responses={
        200: {
            "description": "Succesful operation",
            "content": {
                "application/json": {
                    "example": {
                        "model_name": "example_model",
                        "version": "1.0",
                        "status": "active",
                        "library": "scikit-learn",
                        "libraryVersion": "0.24.1",
                        "domain": "image_classification",
                        "tag": "v1",
                        "parameters": {
                            "batch_size": "50",
                            "learning_rate": "0.2"
                        },
                        "characteristics": {
                            "contamination": "0.03",
                            "accuracy": "0.86"
                        }
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
    status: str = Form(...),
    library: str = Form(...),
    libraryVersion: str = Form(...),
    domain: str = Form(...),
    tag: str = Form(...),
    parameters: str = Form(...),
    characteristics: str = Form(...),
    file: UploadFile = File(...),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session)
):
    try:

        parameters = json.loads(parameters)
        characteristics = json.loads(characteristics)
        
        # Create model instance from parsed fields
        model_data = Model(
            name=name,
            version=version,
            status=status,
            library=library,
            libraryVersion=libraryVersion,
            domain=domain,
            tag=tag,
            parameters=parameters,
            characteristics=characteristics
        )

        logger.info(f"Adding model: {model_data.name}, version: {model_data.version}")

        try:
            minio_path = await minio_operations.upload_file_to_minio(file, minio_session, minio_operations.BUCKET_REGISTRY)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

        model_id = db_actions.save_model(model_data, minio_path, db_session)

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

    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")

    except Exception as e:
        logger.error(f"Error adding model: {e}")
        raise HTTPException(status_code=400, detail="Error adding model")