from typing import Dict
import kfp
from kfp import kubernetes
from kfp.dsl import container_component, ContainerSpec, InputPath, OutputPath, Output, pipeline, If

@container_component
def dataset_creation(
            datasetsharing_api_url: str,
            timescale_db_params: dict,
            dataset_params: dict):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/dataset_creation_and_sharing.py'],
        args=[
            '--datasetsharing_api_url', datasetsharing_api_url,
            '--timescale_db_params', timescale_db_params,
            '--dataset_params', dataset_params,
        ]
    )

@pipeline(
    name='Dataset creation pipeline',
    description='Pipeline to create a dataset.'
)
def pipeline(datasetsharing_api_url: str = "http://datasetsharing-service.default.svc.cluster.local:8080",
            timescale_db_params: dict = {
                "dbname": "ile",
                "user": "admin",
                "password": "admin",
                "host": "timescale-service.default.svc.cluster.local",
                "port": "5432",
            },
            dataset_params: dict = {
                "name": "ispm",
                "version": "1.0.0",
                "dataType": "mixed",
                "tag": "timeseries",
                "parameters": {
                    "description": "compressed pickles files in a zip file",
                    "format": "train_x and train_y dataframes",
                }
            }) -> None:
    
    dataset_creation_stage = dataset_creation(
        timescale_db_params=timescale_db_params,
        datasetsharing_api_url=datasetsharing_api_url,
        dataset_params=dataset_params
    )
    dataset_creation_stage.set_caching_options(False)
    kubernetes.set_image_pull_policy(dataset_creation_stage, "Always")


def main():

    pipeline_file_name = "mno-dataset-creation"
    kfp.compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=f"{pipeline_file_name}.yaml"
    )

    with open(f"{pipeline_file_name}.yaml", "rt") as f:
        print(f.read())

if __name__ == "__main__":
    main()