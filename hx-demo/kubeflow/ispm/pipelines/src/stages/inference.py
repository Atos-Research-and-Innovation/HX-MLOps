import json
import pandas as pd
import psycopg2
import requests
from typing import List
import argparse
import utils
import sys
from wrappers.minio import pipelines_filesystem_conn, upload_local_directory_to_minio, minio_get_folder
import os
import subprocess
import json
import time

def load_data(conn):
    """
    Load data form timescaledb to be preprocessed later.
    """    

    # Load data from timescaledb:
    # Query using heredoc.
    sql_command_X = """
    SELECT
    EXTRACT(EPOCH FROM (timestamp - date_trunc('day', timestamp)))::int AS day_time,
    container_id,
    timestamp,
    CASE WHEN status THEN 1 ELSE 0 END AS status
    FROM
        ile_timeseries
    WHERE
        timestamp = '2024-01-01 00:40:00'
    ORDER BY
        timestamp, container_id;
        """
    
    df_X = pd.read_sql(sql_command_X, conn)
    conn.close()

    return df_X

def structure_data(input_df):

    structured_input_df = input_df.pivot(index=['timestamp', 'day_time'], columns='container_id', values='status')
    structured_input_df.columns = [f'cnt{col}' for col in structured_input_df.columns]
    structured_input_df.reset_index(inplace=True)
    structured_input_df = structured_input_df.drop(columns=['day_time'])
    return structured_input_df

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of adquiring models from other domains via API and storing them in minio.",
    )
    parser.add_argument(
        "--dbname",
        type=str,
        help="database name",
        required=True,
    )
    parser.add_argument(
        "--dbuser",
        type=str,
        help="database user",
        required=True,
    )
    parser.add_argument(
        "--dbpassword",
        type=str,
        help="database password",
        required=True,
    )
    parser.add_argument(
        "--dbhost",
        type=str,
        help="database host",
        required=True,
    )
    parser.add_argument(
        "--dbport",
        type=str,
        help="database port",
        required=True,
    )
    parser.add_argument(
        "--torchserve_inference_url",
        type=str,
        help="torchserve url where do inference (must be included the specific model)",
        required=True,
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:

    args = parse_args(argv)
    dbname = args.dbname
    dbuser = args.dbuser
    dbpassword = args.dbpassword
    dbhost = args.dbhost
    dbport = args.dbport
    torchserve_inference_url = args.torchserve_inference_url

    max_iterations = 10
    sleep_time = 2 

    # Establish connection to PostgreSQL
    conn = psycopg2.connect(
        dbname=dbname,
        user=dbuser,
        password=dbpassword,
        host=dbhost,
        port=dbport
    )

    # Define the URL for the TorchServe endpoint
    # url = "http://[::1]/restinference/predictions/ispm-1"
    url = torchserve_inference_url

    # Create some dummy data for testing
    sample_input_df = load_data(conn)
    sample_str_input_df = structure_data(sample_input_df)
    sample_input = sample_str_input_df.values.tolist()


    for i, input_data in enumerate(sample_input):

        input_data[0] = input_data[0].isoformat()  # Convertir la fecha en formato ISO si es necesario

        print(f"Input data {i}: ", input_data)

        payload = json.dumps([input_data])

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print(f"Inference response {i}: ", response.json())
        else:
            print(f"Failed to get response for input {i}, status code:", response.status_code)
            print(f"Response for input {i}:", response.text)
        
        if i < max_iterations - 1:
            print(f"Waiting for {sleep_time} seconds before next iteration...")
            time.sleep(sleep_time)


if __name__ == "__main__" and "NOTEBOOK" not in globals():
    main(sys.argv[1:])