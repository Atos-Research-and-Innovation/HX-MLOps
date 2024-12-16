"""
model adquisiton stage
====================
"""

import argparse
import utils
import sys
import json
import requests
from wrappers.minio import pipelines_filesystem_conn, upload_local_directory_to_minio, minio_get_folder
import os
import sys
from typing import List
import subprocess
from wrappers.torchserve import send_model_to_torchserve
import json



def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of adquiring models from other domains via API and storing them in minio.",
    )

    parser.add_argument(
        "--torchserve_management_api",
        type=str,
        help="address of the management api. e.g. http://localhost:8081",
        required=True,
    )
    parser.add_argument(
        "--modelsharing_api_url",
        type=str,
        help="address of the management api. e.g. http://localhost:8080",
        required=True,
    )
    parser.add_argument(
        "--model_params",
        type=str,
        help="model parameters to get the model from swv domain",
        required=True,
    )   
    return parser.parse_args(argv)

def main(argv: List[str]) -> None:
    args = parse_args(argv)
    
    model_params = json.loads(args.model_params)
    modelsharing_api_url = args.modelsharing_api_url
    management_api = args.torchserve_management_api
    
    ##############################################################################
    ##############################################################################
    ####--------- get model from swv domain through modelSherving API------#######
    ##############################################################################
    ##############################################################################

    # 1. Check if modelSharing API is available
    endpoint = f"{modelsharing_api_url}/api/v1/health"
    response = requests.get(endpoint)

    if not (response.status_code == 200 and response.json() == {"status": "UP"}):
        print(f"ModelSharing API not available. {response.json()}")
        return 0
    print(f"ModelSharing API available. {response.json()}")
    
    # 2. Get model catalog and select the model to serve
    params_data = {
        "domain": model_params.get("domain", ""),
        "tag": model_params.get("tag", ""),
        "status": model_params.get("status", ""),
        "name": model_params.get("name", ""),
        "version": model_params.get("version", ""),
    }
    print("filters to get models: ", params_data)
    endpoint = f"{modelsharing_api_url}/api/v1/model_catalog"

    response = requests.get(
            endpoint,
            params=params_data,
    )

    if response.status_code != 200:
        print("Response Text:", response.text) 
        print(f"Error download model catalog")
        return 0

    response_data = response.json()
    print(f"Model catalog: {response_data}")
    model_identifier = response_data['models'][0]['modelIdentifier']
    model_version = response_data['models'][0]['version']
    model_name = response_data['models'][0]['name']

    # 3. Download model file
    endpoint = f"{modelsharing_api_url}/api/v1/model/by_id/{model_identifier}"
    params_data = {
        "version": model_version
    }
    response = requests.get(
                    endpoint,
                    params=params_data)

    if response.status_code != 200:
        print("Response Text:", response.text) 
        print(f"Error download model file")
        return 0

    file_path = os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH)
    filename = f"{model_name}-{model_version}"
    filename_with_extension = filename + ".mar"

    os.makedirs(file_path, exist_ok=True)

    with open(os.path.join(file_path, filename_with_extension), "wb") as f:
        f.write(response.content)


    # 4. Serve the model through torchserve
    response = send_model_to_torchserve(management_api=management_api,
                             local_serving_directory=os.path.join(utils.CONTAINER_APP_PATH, utils.CONTAINER_HANDLER_OUTPUT_PATH),
                             archived_model_file_name=filename,
                             torchserve_params={},
                             model_name=model_name,
                             model_version=model_version,
                             timeout=60,
                             port=8222)
    print("Response Text:", response.text)
    response.raise_for_status()
    print("Request was successful!")
    
    

if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])