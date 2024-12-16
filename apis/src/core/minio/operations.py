from minio import Minio
from minio.error import S3Error
import os
import io
import glob
from src.core.logger_session import logger
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import uuid
from io import BytesIO


BUCKET_REGISTRY = os.environ.get("MINIO_BUCKET") or "modelsharing-registry"


def get_session():

    user = os.environ.get("MINIO_USER")
    passwd = os.environ.get("MINIO_PASSWORD")
    host = os.environ.get("MINIO_URL")
    port = os.environ.get("MINIO_PORT")

    client = Minio(f"{host}:{port}", user, passwd, secure=False)

    return client


def check_connection():
    try:
        client = get_session()
        buckets = client.list_buckets()
        return True
    except S3Error as e:
        return False


def create_bucket(client, bucket_name):
    """
    Function that checks if a bucket with the
    user name exists, if not creates one.
    """

    try:
        logger.info(f"creating bucket {bucket_name} ...")
        if client.bucket_exists(bucket_name):
            logger.info(f"{bucket_name} bucket already exists")
        else:
            # Create bucket.
            client.make_bucket(bucket_name)
            logger.info(f" {bucket_name} bucket created")
    except S3Error as e:
        logger.exception(f"Error creating bucket: {e}")


async def upload_file_to_minio(file: UploadFile, minio_client, bucket) -> str:
    try:
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_content = await file.read()

        minio_client.put_object(bucket, unique_filename, BytesIO(file_content), len(file_content))

        return f"{bucket}/{unique_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to MinIO: {str(e)}")


def get_file_from_minio(file_path: str, minio_client):
    try:
        # Split the string by the first occurrence of '/'
        split_path = file_path.split("/", 1)

        bucket_name = split_path[0]
        object_path = split_path[1]
        
        data = minio_client.get_object(bucket_name, object_path)
        return data
    except S3Error as e:
        raise HTTPException(status_code=404, detail="Model file not found in MinIO") from e


def delete_object(minio_session, file_path: str):
    try:
        # Split the string by the first occurrence of '/'
        split_path = file_path.split("/", 1)

        bucket_name = split_path[0]
        object_path = split_path[1]
        minio_session.remove_object(bucket_name, object_path)
    except Exception as e:
        raise Exception(f"Error deleting file from MinIO: {str(e)}")