from src.api.modelsharing.schemas.addModel import ModelResponse
from src.api.modelsharing.schemas.modelCatalog import ModelCatalogResponse
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.modelsharing.database import actions as db_actions
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session


router = APIRouter()

@router.get(
    "/model_catalog",
    tags=["model"],
    summary="Get model catalog by filters",
    description="Service to get a model catalog based on provided filters such as domain, class, tag, and status.",
    operation_id="getModelCatalog",
    response_model=ModelCatalogResponse,
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ModelCatalog"  # Ref al esquema que definiste
                    }
                }
            }
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "Model not found"},
    },
)
async def get_model_catalog(
    domain: Optional[str] = Query(None, description="Filter models by domain"),
    tag: Optional[str] = Query(None, description="Filter models by tag"),
    status: Optional[str] = Query("production", description="Filter models by status", enum=["production", "staging", "development"]),
    name: Optional[str] = Query(None, description="Filter models by name"),
    version: Optional[str] = Query(None, description="Filter models by version"),
    db_session: Session = Depends(db_operations.get_session),
):
    models_data = db_actions.get_filtered_models(db_session, domain, tag, status, name, version)
    
    if not models_data:
        raise HTTPException(status_code=404, detail="No models found matching the filters")

    responses = []
    for model in models_data:
        modelres = ModelResponse(
            modelIdentifier=model.id,
            name=model.name,
            version=model.version,
            status=model.status,
            library=model.library,
            libraryVersion=model.libraryVersion,
            domain=model.domain,
            tag=model.tag,
            parameters=model.parameters,
            characteristics=model.characteristics
        )
        responses.append(modelres)

    
    return ModelCatalogResponse(models=responses)
