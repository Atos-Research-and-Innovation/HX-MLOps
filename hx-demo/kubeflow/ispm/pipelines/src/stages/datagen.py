"""
Data generation stage
====================

"""

import argparse
import os
import sys
from typing import List
from wrappers.minio import pipelines_filesystem_conn, minio_create_bucket, minio_create_directory, upload_local_directory_to_minio, minio_get_folder
import utils
import json


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of generating data which will be used to train the model.",
    )
    parser.add_argument(
        "--minio_params",
        type=str,
        help="Name of the pipeline.",
        required=True,
    )
    parser.add_argument(
        "--datagen_params",
        type=str,
        help="user params.",
        required=True,
    )
    return parser.parse_args(argv)

def main(argv: List[str]) -> None:
    args = parse_args(argv)
    
    minio_params = json.loads(args.minio_params)
    minio_host = minio_params["host"]
    minio_port = minio_params["port"]
    minio_user = minio_params["user"]
    minio_password = minio_params["password"]
    bucket_name = minio_params["bucket_name"]
    
    client = pipelines_filesystem_conn(minio_host,
                                       minio_port,
                                       minio_user,
                                       minio_password)
    
    # minio create buckets and directories if does not exist
    minio_create_bucket(client, bucket_name)
    minio_create_directory(client, bucket_name, utils.MINIO_DATA_PATH)
    minio_create_directory(client, bucket_name, utils.MINIO_CODE_PATH)
    minio_create_directory(client, bucket_name, utils.MINIO_MODEL_OUTPUT_PATH)
    minio_create_directory(client, bucket_name, utils.MINIO_HANDLER_OUTPUT_PATH)

    
    # Download the user's code from minio
    minio_get_folder(
        client,
        bucket_name=bucket_name,
        minio_path=utils.MINIO_CODE_PATH,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_CODE_PATH))
    
    # import file where user write their code for datagen_pipeline
    datagen_pipeline = getattr(__import__(utils.CONTAINER_CODE_PATH, fromlist=[utils.DATAGEN_FILENAME]), utils.DATAGEN_FILENAME)
    args_main = [
            '--datagen_params', args.datagen_params
    ]
    datagen_pipeline.main(args_main)
    
    
    upload_local_directory_to_minio(
        client,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_DATA_PATH),
        bucket_name=bucket_name,
        minio_path=utils.MINIO_DATA_PATH
    )

if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])