from typing import Dict
import kfp
from kfp import kubernetes
from kfp.dsl import container_component, ContainerSpec, InputPath, OutputPath, Output, pipeline, If


@container_component
def datagen(minio_params: dict,
            datagen_params: dict):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/datagen.py'],
        args=[
            '--minio_params', minio_params,
            '--datagen_params', datagen_params,
        ]
    )
    
@container_component
def trainer(minio_params: dict):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/trainer.py'],
        args=[
            '--minio_params', minio_params,
        ]
    )


@container_component
def eval(minio_params: dict,
        eval_output: OutputPath(str)):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/eval.py'],
        args=[
            '--minio_params', minio_params,
            '--eval_output', eval_output
        ],
    )
    

@container_component
def pusher(modelsharing_api_url: str,
            torchserve_params: dict,
            minio_params: dict,
            pusher_params: dict):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/pusher.py'],
        args=[
            '--modelsharing_api_url',  modelsharing_api_url,
            '--minio_params', minio_params,
            '--torchserve_params', torchserve_params,
            '--pusher_params', pusher_params
        ]
    )


@pipeline(
    name='pytorch cpu pipeline',
    description='Training pipeline SWV domain (ISPM model)'
)
def pipeline(modelsharing_api_url: str = "http://modelsharing-service.default.svc.cluster.local:8080",
            torchserve_params: dict = {
                "torchserve_management_api": "http://torchserve-service-rest-managment.default:8081",
                "nn_file_path": "models/initialDNN.py",
                "model_output_filename": "model.pth",

            },
            minio_params: dict = {
                "host": "minio-service-api.default.svc.cluster.local",
                "port": "9000",
                "user":"minio",
                "password": "minio123",
                "bucket_name": "code-repository"
            },
            pusher_params: dict = {
                "name": "ispm",
                "version": "1.0.0",
                "status": "production",
                "library": "pytorch",
                "libraryVersion": "0.24",
                "domain": "deeplearning",
                "tag": "neuralNetwork",
                "parameters": {"learning_rate": 0.01,
                    "batch_size": 64,
                    "epochs": 10,
                    "optimizer": "adam",
                    "momentum": 0.9
                },
            },
            datagen_params: dict = {}) -> None:
    
    generate_data_stage = datagen(
        minio_params=minio_params,
        datagen_params=datagen_params,
    )
    generate_data_stage.set_caching_options(False)
    kubernetes.set_image_pull_policy(generate_data_stage, "Always")
    
    generate_trainer_stage = trainer(
        minio_params=minio_params
    )
    generate_trainer_stage.set_caching_options(False)
    generate_trainer_stage.after(generate_data_stage)
    kubernetes.set_image_pull_policy(generate_trainer_stage, "Always")


    generate_eval_stage = eval(
        minio_params=minio_params
    )
    generate_eval_stage.set_caching_options(False)
    generate_eval_stage.after(generate_trainer_stage)
    kubernetes.set_image_pull_policy(generate_eval_stage, "Always")

    with If(generate_eval_stage.outputs["eval_output"] == 'ok'):
        generate_pusher_stage = pusher(
            minio_params=minio_params,
            modelsharing_api_url=modelsharing_api_url,
            torchserve_params=torchserve_params,
            pusher_params=pusher_params
        )
        generate_pusher_stage.set_caching_options(False)
        generate_pusher_stage.after(generate_eval_stage)
        kubernetes.set_image_pull_policy(generate_pusher_stage, "Always")


def main():

    pipeline_file_name = "swv-training"
    kfp.compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=f"{pipeline_file_name}.yaml"
    )

    with open(f"{pipeline_file_name}.yaml", "rt") as f:
        print(f.read())

if __name__ == "__main__":
    main()