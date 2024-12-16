from src.api.modelsharing.schemas.health import HealthResponse, HealthStatus
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations

from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/health", 
    responses={
        200: {
            "description": "Successful operation",
            "content": {"application/json": {"example": {"status": "UP"}}}
        },
        400: {
            "description": "Bad Request",
        },
        403: {
            "description": "Forbidden Request",
        },
        404: {
            "description": "Service status not found",
        }
    },
    response_model=HealthResponse,
    tags=["health"],
    summary="Test service Health",
    operation_id="getHealth",
    description="Service Health Check"
    )
async def root():
    logger.info("/health endpoint invoked")
    result_db = db_operations.check_connection()
    result_minio = minio_operations.check_connection()

    if result_db and result_minio:
        logger.info(f"/health api {HealthStatus.UP}")
        return HealthResponse(status=HealthStatus.UP)

    logger.warning(f"/health api {HealthStatus.DOWN}")
    return HealthResponse(status=HealthStatus.DOWN)