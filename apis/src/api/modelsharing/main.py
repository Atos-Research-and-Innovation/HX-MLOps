from src.api.modelsharing.endpoints.health import router as health_router
from src.api.modelsharing.endpoints.add_model import router as add_model_router
from src.api.modelsharing.endpoints.get_model_by_id_and_version import router as get_model_by_id_and_version_router
from src.api.modelsharing.endpoints.delete_model_by_id_and_version import router as delete_model_by_id_and_version_router
from src.api.modelsharing.endpoints.get_model_info import router as get_model_info_router
from src.api.modelsharing.endpoints.get_model_catalog import router as get_model_catalog
from src.core.logger_session import logger
from src.core.timescaledb import operations as db_operations
from src.core.minio import operations as minio_operations
from src.api.modelsharing.database.model import Base as modelsharingBase

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import pandas as pd


from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

db_operations.create_db()
db_operations.create_tables(modelsharingBase)

minio_client = minio_operations.get_session()
minio_operations.create_bucket(minio_client, minio_operations.BUCKET_REGISTRY)


app = FastAPI(
    title="Machine Learning Model Sharing - OpenAPI 3.0",
    description="Machine Learning Model Sharing OpenAPI definition",
    version="1.0.0",
    terms_of_service="http://swagger.io/terms/",
    contact={
        "email": "imasd@optaresolutions.org",
        "email2": "joaquin.caceres@eviden.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
    external_docs={
        "description": "HexaX II Project Link",
        "url": "https://hexa-x-ii.eu/"
    }
)


app.include_router(get_model_catalog, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(add_model_router, prefix="/api/v1")
app.include_router(delete_model_by_id_and_version_router, prefix="/api/v1")
app.include_router(get_model_by_id_and_version_router, prefix="/api/v1")
app.include_router(get_model_info_router, prefix="/api/v1")