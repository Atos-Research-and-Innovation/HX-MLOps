"""
serving stage
====================
"""

import argparse
import utils
import sys
from wrappers.minio import pipelines_filesystem_conn, upload_local_directory_to_minio, minio_get_folder
import os
import sys
from typing import List
import subprocess
from wrappers.torchserve import send_model_to_torchserve
import json


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of serving a model previously trained.",
    )
    parser.add_argument(
        "--swv_bucket",
        type=str,
        help="Name of the bucket where models are stored (swv domain).",
        required=True,
    )
    parser.add_argument(
        "--model_version",
        type=str,
        help="model's version to download",
        required=True,
    )
    parser.add_argument(
        "--minio_host",
        type=str,
        help="minio host",
        required=True,
    )
    parser.add_argument(
        "--minio_port",
        type=str,
        help="minio port",
        required=True,
    )
    parser.add_argument(
        "--minio_user",
        type=str,
        help="minio user",
        required=True,
    )
    parser.add_argument(
        "--minio_password",
        type=str,
        help="minio password",
        required=True,
    )
    parser.add_argument(
        "--torchserve_management_api",
        type=str,
        help="address of the management api. e.g. http://localhost:8081",
        required=True,
    )
    return parser.parse_args(argv)

def main(argv: List[str]) -> None:
    args = parse_args(argv)
    
    # minio arguments and initialise connection:
    minio_host = args.minio_host
    minio_port = args.minio_port
    minio_user = args.minio_user
    minio_password =  args.minio_password
    swv_bucket = args.swv_bucket
    model_version = args.model_version
    management_api = args.torchserve_management_api


    client = pipelines_filesystem_conn(minio_host,
                                       minio_port,
                                       minio_user,
                                       minio_password)


    # download the model from MINIO
    minio_get_folder(
        client,
        bucket_name=swv_bucket,
        minio_path=os.path.join(model_version, utils.MINIO_HANDLER_OUTPUT_PATH),
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH))
    
    

    # Serve the model through torchserve
    handler_file_name = f"{swv_bucket}-{model_version}"
    send_model_to_torchserve(management_api=management_api,
                             local_serving_directory=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH),
                             archived_model_file_name=handler_file_name,
                             torchserve_params={},
                             timeout=60,
                             port=8222)
    
    

if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])
