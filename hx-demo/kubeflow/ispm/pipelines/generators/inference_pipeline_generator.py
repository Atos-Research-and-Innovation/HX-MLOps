from typing import Dict
import kfp
from kfp import kubernetes
from kfp.dsl import container_component, ContainerSpec, pipeline

@container_component
def inference(dbname: str,
            dbuser: str,
            dbpassword: str,
            dbhost: str,
            dbport: str,
            torchserve_inference_url: str):
    return kfp.dsl.ContainerSpec(
        image='localhost:32000/smlops-hexa-x-ii:1.0.0',
        command=['python', '/app/stages/inference.py'],
        args=[
            '--dbname', dbname,
            '--dbuser', dbuser,
            '--dbpassword', dbpassword,
            '--dbhost', dbhost,
            '--dbport', dbport,
            '--torchserve_inference_url', torchserve_inference_url,
        ]
    )

@pipeline(
    name='inference ispm pipeline',
    description='Pipeline to apply inference over ISPM model.'
)
def pipeline(dbname: str = "ile",
            dbuser: str = "admin",
            dbpassword: str = "admin",
            dbhost: str = "timescale-service.default.svc.cluster.local",
            dbport: str = "5432",
            torchserve_inference_url: str = "http://torchserve-service-rest-inference.default.svc.cluster.local:8080/predictions/ispm") -> None:
    
    inference_adquisition_stage = inference(
        dbname=dbname,
        dbuser=dbuser,
        dbpassword=dbpassword,
        dbhost=dbhost,
        dbport=dbport,
        torchserve_inference_url=torchserve_inference_url)

    inference_adquisition_stage.set_caching_options(False)
    kubernetes.set_image_pull_policy(inference_adquisition_stage, "Always")


def main():

    pipeline_file_name = "mno-inference"
    kfp.compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=f"{pipeline_file_name}.yaml"
    )

    with open(f"{pipeline_file_name}.yaml", "rt") as f:
        print(f.read())

if __name__ == "__main__":
    main()