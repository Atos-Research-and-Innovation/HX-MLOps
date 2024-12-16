from typing import Dict
import kfp
from kfp import kubernetes
from kfp.dsl import container_component, ContainerSpec, InputPath, OutputPath, Output, pipeline, If

@container_component
def model_adquisition_and_serving(
            torchserve_management_api: str,
            modelsharing_api_url: str,
            model_params: dict):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/model_adquisition_and_serving.py'],
        args=[
            '--torchserve_management_api', torchserve_management_api,
            '--modelsharing_api_url', modelsharing_api_url,
            '--model_params', model_params,
        ]
    )

@pipeline(
    name='Model adquisition and serving pipeline',
    description='Pipeline to get the model from Software Vendor Domain through ModelSharing API and serve it in torchserve component .'
)
def pipeline(torchserve_management_api: str = "http://torchserve-service-rest-managment.default:8081",
            modelsharing_api_url: str = "http://13.39.193.167:30081",
            model_params: dict = {
                "domain": "deeplearning",
                "tag": "neuralNetwork",
                "status": "production",
                "name": "ispm",
                "version": "1.0.0",
            }) -> None:
    
    model_adquisition_stage = model_adquisition_and_serving(
        torchserve_management_api=torchserve_management_api,
        modelsharing_api_url=modelsharing_api_url,
        model_params=model_params
    )
    model_adquisition_stage.set_caching_options(False)
    kubernetes.set_image_pull_policy(model_adquisition_stage, "Always")


def main():

    pipeline_file_name = "mno-serving"
    kfp.compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=f"{pipeline_file_name}.yaml"
    )

    with open(f"{pipeline_file_name}.yaml", "rt") as f:
        print(f.read())

if __name__ == "__main__":
    main()