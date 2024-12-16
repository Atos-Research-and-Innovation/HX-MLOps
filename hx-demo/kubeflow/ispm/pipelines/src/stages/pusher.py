"""
pushing stage
====================
"""

import argparse
import utils
import sys
from wrappers.minio import pipelines_filesystem_conn, upload_local_directory_to_minio, minio_get_folder
import os
import json
from typing import List
import subprocess
from wrappers.torchserve import send_model_to_torchserve
import requests
import json


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of serving a model previously trained.",
    )
    parser.add_argument(
        "--modelsharing_api_url",
        type=str,
        help="address of the management api. e.g. http://localhost:8080",
        required=True,
    )
    parser.add_argument(
        "--minio_params",
        type=str,
        help="Name of the pipeline.",
        required=True,
    )
    parser.add_argument(
        "--pusher_params",
        type=str,
        help="api parameters to add model to the registry",
        required=True,
    )
    parser.add_argument(
        "--torchserve_params",
        type=str,
        help="torchserve params neccesary to create .mar handler file",
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

    torchserve_params = json.loads(args.torchserve_params)
    management_api = torchserve_params["torchserve_management_api"]
    model_output_filename = torchserve_params["model_output_filename"]
    nn_file_path = torchserve_params["nn_file_path"]
    pusher_params = json.loads(args.pusher_params)
    modelsharing_api_url = args.modelsharing_api_url
    
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
    
    # Download the model previously trained by user
    minio_get_folder(
        client,
        bucket_name=bucket_name,
        minio_path=utils.MINIO_MODEL_OUTPUT_PATH,
        local_path=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_MODEL_OUTPUT_PATH))
    
    # create directory to store the handler.mar file:
    path = os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH)
    if not os.path.exists(path):
        os.makedirs(path)


    # Archive the model
    model_version = pusher_params["version"]
    model_name = pusher_params["name"]
    handler_file_name = f"{model_name}-{model_version}"
    result = subprocess.run(
        [
            "torch-model-archiver",
            "--model-name",
            handler_file_name,
            "--model-file",
            os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_CODE_PATH, nn_file_path),
            "--handler",
            os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_CODE_PATH, utils.HANDLER_FILENAME),
            "--version",
            pusher_params["version"],
            "--serialized-file",
            os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_MODEL_OUTPUT_PATH, model_output_filename),
            "--export-path",
            os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH),
            
        ],
        check=True,
    )

    ##############################################################################
    ##############################################################################
    ####--------- push torch model to registry using modelsharing API-------#######
    ##############################################################################
    ##############################################################################

    endpoint = f"{modelsharing_api_url}/api/v1/health"
    response = requests.get(endpoint)

    if not (response.status_code == 200 and response.json() == {"status": "UP"}):
        print(f"ModelSharing API not available. {response.json()}")

    else:
        print(f"ModelSharing API available. {response.json()}")
        test_data = {
            "name": pusher_params["name"],
            "version": pusher_params["version"],
            "status": pusher_params["status"],
            "library": pusher_params["library"],
            "libraryVersion": pusher_params["libraryVersion"],
            "domain": pusher_params["domain"],
            "tag": pusher_params["tag"],
            "parameters": pusher_params.get("parameters", {}),
            "characteristics": pusher_params.get("characteristics", {}),
        }

        endpoint = f"{modelsharing_api_url}/api/v1/model"

        parameters_json = json.dumps(test_data["parameters"])
        characteristics_json = json.dumps(test_data["characteristics"])

        data = {
            "name": test_data["name"],
            "version": test_data["version"],
            "status": test_data["status"],
            "library": test_data["library"],
            "libraryVersion": test_data["libraryVersion"],
            "domain": test_data["domain"],
            "tag": test_data["tag"],
            "parameters": parameters_json,
            "characteristics": characteristics_json,
        }

        filename = handler_file_name + ".mar"
        file_path = os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH, filename)
        with open(file_path, 'rb') as f:
            files = {
                "file": (filename , f, "application/octet-stream")
            }

            response = requests.post(
                endpoint,
                data=data,
                files=files
            )


            if response.status_code == 200:
                response_data = response.json()
                print(f"Model add to the registry. {response_data}")
            else:
                print(f"Error adding the model to the registry")


if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])