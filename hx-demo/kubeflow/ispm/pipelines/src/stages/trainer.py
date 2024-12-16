"""
Trainer stage
====================

"""

import argparse
import os
import sys
import utils
from typing import List
from wrappers.minio import pipelines_filesystem_conn, upload_local_directory_to_minio, minio_get_folder
import json

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of train a model.",
    )
    parser.add_argument(
        "--minio_params",
        type=str,
        help="Name of the pipeline.",
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
    
    # Download the user's code from minio 
    minio_get_folder(
        client,
        bucket_name=bucket_name,
        minio_path=utils.MINIO_CODE_PATH,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_CODE_PATH))
    
    
    minio_get_folder(
        client,
        bucket_name=bucket_name,
        minio_path=utils.MINIO_DATA_PATH,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_DATA_PATH))
    

    # import file where user write their code for trainer_pipeline
    trainer_pipeline = getattr(__import__(utils.CONTAINER_CODE_PATH, fromlist=[utils.TRAINER_FILENAME]), utils.TRAINER_FILENAME)
    trainer_pipeline.main()
    
    upload_local_directory_to_minio(
        client,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_MODEL_OUTPUT_PATH),
        bucket_name=bucket_name,
        minio_path=utils.MINIO_MODEL_OUTPUT_PATH
    )

if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])