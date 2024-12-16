import os
import pandas as pd
import psycopg2
import numpy as np
import zipfile
import requests
import json
import argparse
import sys

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy import func, case, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List

Base = declarative_base()

class IleTimeseries(Base):
    __tablename__ = 'ile_timeseries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(String)
    timestamp = Column(DateTime)
    status = Column(Boolean)
    ground_truth = Column(Boolean)


def query_x(session):
    query_x = (
        session.query(
            (func.extract('epoch', IleTimeseries.timestamp - func.date_trunc('day', IleTimeseries.timestamp)).cast(Integer)).label('day_time'),
            IleTimeseries.container_id,
            IleTimeseries.timestamp,
            case(
                (IleTimeseries.status == True, 1),
                else_=0
            ).label('status'),
        )
        .order_by(IleTimeseries.timestamp, IleTimeseries.container_id)
    )
    return query_x

def query_y(session):
    query_y = (
        session.query(
            IleTimeseries.container_id,
            IleTimeseries.timestamp,
            case(
                (IleTimeseries.ground_truth == True, 1),
                else_=0 
            ).label('ground_truth')
        )
        .order_by(IleTimeseries.timestamp, IleTimeseries.container_id)
    )
    return query_y

def dataframe_to_description(df):
    return {
        "shape": df.shape,  # Número de filas y columnas
        "columns": list(df.columns),  # Nombres de columnas
        "dtypes": df.dtypes.astype(str).to_dict(),  # Tipos de datos por columna
        "preview": df.head(5).applymap(
            lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x
        ).to_dict(orient="records"),  # Vista previa con fechas serializadas
    }

class CustomError(Exception):
    def __init__(self, response_data):
        self.response_data = response_data
        super().__init__(str(response_data))


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Module in charge of create a dataset.",
    )
    parser.add_argument(
        "--datasetsharing_api_url",
        type=str,
        help="address of the management api. e.g. http://localhost:8080",
        required=True,
    )
    parser.add_argument(
        "--timescale_db_params",
        type=str,
        help="Timescale DB parameters.",
        required=True,
    )
    parser.add_argument(
        "--dataset_params",
        type=str,
        help="torchserve params neccesary to create .mar handler file",
        required=True,
    )   

    return parser.parse_args(argv)

    
def main(argv: List[str]):
    args = parse_args(argv)

    timescale_db_params = json.loads(args.timescale_db_params)
    dataset_params = json.loads(args.dataset_params)
    datasetsharing_api_url = args.datasetsharing_api_url
    dbname = timescale_db_params["dbname"]
    user = timescale_db_params["user"]
    password = timescale_db_params["password"]
    host = timescale_db_params["host"]
    port = timescale_db_params["port"]

    dataset_params = {
        "name": dataset_params ["name"],
        "version": dataset_params ["version"],
        "dataType": dataset_params ["dataType"],
        "tag": dataset_params ["tag"],
        "parameters": json.dumps(dataset_params.get("parameters", {}))
    }


    engine = create_engine(f"postgresql://{user}:{password}@{host}/{dbname}")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    q_x = query_x(session)
    q_y = query_y(session)
    df_X = pd.read_sql(q_x.statement, session.bind)
    df_y = pd.read_sql(q_y.statement, session.bind)
    session.close()


    data_model = {
        "df_X": dataframe_to_description(df_X),
        "df_y": dataframe_to_description(df_y)
    }

    # -------------saving data---------------------------------------
    
    data_path = "/app/data"
    os.makedirs(data_path, exist_ok=True)

    X_train_file = "X_train.pkl"
    Y_train_file = "y_train.pkl"
    zip_file = "dataset.zip"
    data_model_file = "data_model.json"

    X_train_path = os.path.join(data_path, X_train_file)
    Y_train_path = os.path.join(data_path, Y_train_file)
    zip_file_path = os.path.join(data_path, zip_file)
    data_model_path = os.path.join(data_path, data_model_file)


    with open(data_model_path, "w") as f:
        json.dump(data_model, f, indent=4)


    df_X.to_pickle(X_train_path)
    df_y.to_pickle(Y_train_path) 

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(X_train_path, arcname=X_train_file)
        zipf.write(Y_train_path, arcname=Y_train_file)


    # 1. Check if modelSharing API is available
    endpoint = f"{datasetsharing_api_url}/api/v1/health"
    response = requests.get(endpoint)

    if not (response.status_code == 200 and response.json() == {"status": "UP"}):
        print(f"DatasetSharing API not available. {response.json()}")
        return 0
    print(f"DatasetSharing API available. {response.json()}")

    # 2. add dataset to registry
    with open(zip_file_path, 'rb') as f_zip, open(data_model_path, 'rb') as f_data_model:
        files = {
            "dataModelFile": (data_model_file , f_data_model, "application/octet-stream"),
            "datasetFile":  (zip_file , f_zip, "application/octet-stream"),
        }

        endpoint = f"{datasetsharing_api_url}/api/v1/dataset"
        response = requests.post(
            endpoint,
            data=dataset_params,
            files=files
        )

    if response.status_code == 200:
        response_data = response.json()
        print(f"catalog add to the registry. {response_data}")
    else:
        error_message = "Error adding the dataset to the registry"
        print(error_message)
        raise CustomError(response.json())


if __name__ == "__main__" and "NOTEBOOK" not in globals():
    test = False

    if not test:
        main(sys.argv[1:])

    else:

        datasetsharing_api_url = "http://datasetsharingapi.hexaxii.com:8080"
        timescale_db_params = json.dumps({
            "dbname": "ile",
            "user": "admin",
            "password": "admin",
            "host": "timescaledb.hexaxii.com",
            "port": "5432",
        })
        dataset_params = json.dumps({
            "name": "ispm",
            "version": "1.0.0",
            "dataType": "mixed",
            "tag": "timeseries",
            "parameters": {
                "description": "compressed pickles files in a zip file",
                "format": "train_x and train_y dataframes",
            }
        })


        args = [
            '--datasetsharing_api_url', datasetsharing_api_url,
            '--timescale_db_params', timescale_db_params,
            '--dataset_params', dataset_params
        ]
        main(args)