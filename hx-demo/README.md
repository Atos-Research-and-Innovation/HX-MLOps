# Commands to deploy the MLOps environment
0.  python3 -m mlopsTool init set_default_domain
1.  python3 -m mlopsTool component storage create minio
2.  python3 -m mlopsTool component storage create timescale
3.  python3 -m mlopsTool component ml_toolkit create kubeflowPipeline
4.  python3 -m mlopsTool component serving_platform create torchserve
5.  python3 -m mlopsTool link api create modelsharing
6.  python3 -m mlopsTool link api create datasetsharing


kind load docker-image pytorch-cpu-pipeline-hexa:1.0.0 --name swv
kind load docker-image modelsharing-api:1.0.0 --name swv


# postgres:

psql -h localhost -U admin -p 30099 -d ile
psql -h localhost -d ile -U admin -p 30099 -f hx-demo/postgres/dump_withgt_2024-07-29_09_39_53.sql



# torchserver

curl http://localhost/restmanagment/models/ispm/all
curl -X DELETE http://localhost/restmanagment/models/ispm/1.1.1


# modelsharing

http://localhost/modelsharing/api/v1/model/1/data?version=1.0.0
http://localhost/modelsharing/api/v1/model_catalog
http://localhost/modelsharing/api/v1/health



docker save -o smlops-hexa-x-ii.tar smlops-hexa-x-ii:1.0.0
docker save -o modelsharing-api.tar modelsharing-api:1.0.0

docker tag 23232232 smlops-hexa-x-ii:1.0.0


kubectl config use-context opt-machine1
kubectl config get-contexts 
source venv/bin/activate




scp modelsharing-api.tar ubuntu@opt_machine1:/home/ubuntu/atos


# registry

curl -X GET http://localhost:32000/v2/_catalog  -> te devuelve el catalogo de imágenes
curl -X GET http://localhost:32000/v2/pytorch-cpu-pipeline-hexa/tags/list  -> te lista las tag de una imagen 

curl -X GET http://localhost:32000/v2/pytorch-cpu-pipeline-hexa/manifests/1.0.0 -> te lista los parametros de una imagen (digest)
curl -X DELETE http://localhost:32000/v2/nginx/manifests/{digest} -> borrar la imagen con el digest

registry garbage-collect /etc/docker/registry/config.yml



13.39.193.167:32000/smlops-hexa-x-ii:1.0.0 --> MNO

ec2-13-39-193-167.eu-west-3.compute.amazonaws.com:32000/smlops-hexa-x-ii:1.0.0 --> SWV



"params_data" : {
    "name": "ispm",
    "version": "1.0.0"
},
"datasetsharing_api_url" : "http://35.180.23.92:30081"