# Purpose

This folder contains 3 kind config files in order to build a simulation of Telco Environment


# How to build the environment

1. Install kind software: https://kind.sigs.k8s.io/docs/user/quick-start/
2. Use each kind file to set up a new kubernetes cluster:
   1. kind create cluster --config (software-vendor.yaml, mno-staging.yaml or mno-production.yaml)

Useful commands:
    - kind get clusters
    - kind delete cluster --name {cluster name}
