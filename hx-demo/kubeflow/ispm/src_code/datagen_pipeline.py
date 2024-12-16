
import pandas as pd
import psycopg2
import numpy as np
import zipfile
import os
import sys
import requests
import argparse
import json
from typing import List

def unzip_file(zip_file_path, extract_to_path):
    if not os.path.exists(extract_to_path):
        os.makedirs(extract_to_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)



def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of getting data from MNO environment.",
    )
    parser.add_argument(
        "--datagen_params",
        type=str,
        help="user params.",
        required=True,
    )
    return parser.parse_args(argv)
    
    
def main(argv: List[str]):
    """
    Download dataset from MNO domain through dataset sharing API.
    """
    args = parse_args(argv)
    datagen_params = json.loads(args.datagen_params)

    params_data = datagen_params["params_data"]
    datasetsharing_api_url = datagen_params["datasetsharing_api_url"]

    # 1. Check if datasetSharing API is available
    endpoint = f"{datasetsharing_api_url}/api/v1/health"
    response = requests.get(endpoint)

    if not (response.status_code == 200 and response.json() == {"status": "UP"}):
        print(f"DatasetSharing API not available. {response.json()}")
        return 0
    print(f"DatasetSharing API available. {response.json()}")


    # 2. Get dataset catalog and select a specific dataset
    print("filters to get datasets: ", params_data)
    endpoint = f"{datasetsharing_api_url}/api/v1/dataset_catalog"

    response = requests.get(
            endpoint,
            params=params_data,
    )

    if response.status_code != 200:
        print("Response Text:", response.text) 
        print("Error download dataset catalog")
        raise "Error download dataset catalog"

    response_data = response.json()
    print(f"Dataset catalog: {response_data}")
    dataset_identifier = response_data['datasets'][0]['datasetIdentifier']
    dataset_version = response_data['datasets'][0]['version']
    dataset_name = response_data['datasets'][0]['name']


    # 3. Download dataset
    endpoint = f"{datasetsharing_api_url}/api/v1/dataset/by_id/{dataset_identifier}"
    params_data = {
        "version": dataset_version
    }
    response = requests.get(
                    endpoint,
                    params=params_data)

    if response.status_code != 200:
        print("Response Text:", response.text) 
        print(f"Error download dataset file")
        raise "Error download dataset file"

    file_path = "/app/data"
    filename = f"{dataset_name}-{dataset_version}"
    filename_with_extension = filename + ".zip"

    os.makedirs(file_path, exist_ok=True)

    with open(os.path.join(file_path, filename_with_extension), "wb") as f:
        f.write(response.content)

    unzip_file(os.path.join(file_path, filename_with_extension), file_path)
    unzip_file(os.path.join(file_path, "dataset"), file_path)


if __name__ == "__main__" and "NOTEBOOK" not in globals():
    test = True

    if not test:
        main(sys.argv[1:])

    else:

        datagen_params = json.dumps({
            "params_data" : {
                "name": "ispm",
                "version": "1.0.0",
            },
            "datasetsharing_api_url" : "http://datasetsharingapi.hexaxii.com:8080"
        })
        

        args = [
            '--datagen_params', datagen_params
        ]
        main(args)