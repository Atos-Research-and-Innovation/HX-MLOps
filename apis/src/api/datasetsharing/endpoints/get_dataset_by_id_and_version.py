from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
import os
import zipfile
from src.core.logger_session import logger
from src.core.minio import operations as minio_operations
from src.core.timescaledb import operations as db_operations
from src.api.datasetsharing.database import actions as db_actions

router = APIRouter()

@router.get(
    "/dataset/by_id/{dataset_id}",
    tags=["dataset"],
    summary="Get dataset by ID and version",
    description="Service to get a dataset by dataset ID and version (default value 'latest')",
    response_description="dataset files: dataset and dataset description",
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"},
                    "example": "dataset.zip",
                }
            },
        },
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden Request"},
        404: {"description": "dataset not found"},
    },
)
async def get_dataset(
    dataset_id: str,
    version: str = Query("latest", description="dataset version"),
    db_session=Depends(db_operations.get_session),
    minio_session=Depends(minio_operations.get_session)
):
    try:
        dataset_data = db_actions.get_dataset_by_id_and_version(dataset_id, version, db_session)

        dataset_path = dataset_data.datasetPath 
        dataModel_path = dataset_data.dataModelPath
        dataset_file = minio_operations.get_file_from_minio(dataset_path, minio_session)
        dataModel_file = minio_operations.get_file_from_minio(dataModel_path, minio_session)


        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            zip_file.writestr(f"dataset", dataset_file.read())
            zip_file.writestr(f"dataModel", dataModel_file.read())

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={dataset_data.name}_{dataset_data.version}_files.zip"}
        )

        return StreamingResponse(file, media_type="application/octet-stream")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")