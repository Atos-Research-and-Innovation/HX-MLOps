# HX-MLOps

## Table of Contents

<!-- toc -->

- [HX-MLOps introduction](#introduction)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Install with a single command](#install-with-a-single-command)

<!-- tocstop -->


## Introduction

The HX-MLOps software is designed to streamline, oversee, and enhance the lifecycle of AI/ML-driven network services, leveraging established DevOps principles for continuous integration and development (CI/CD) of AI/ML models while addressing the multi-stakeholder nature of the telco-grade ecosystem. It features a Python-based command-line interface (CLI) that allows users—including network operators, vertical industries, and network service developers—to customize and deploy AI/ML workflows tailored to their specific needs. Additionally, it provides a graphical user interface (GUI) for visualizing energy consumption across different stages and components of the workflows. The tool enables the measurement of energy usage and carbon emissions at various stages, empowering users to evaluate and reduce the environmental footprint associated with training, deploying, and utilizing AI/ML assets. The HX-MLOps platform supports modular deployments through a categorized approach to components, including storage solutions, ML lifecycle management modules, serving platforms, observability tools, and energy measurement resources. It also offers APIs for sharing models and datasets among the diverse stakeholders involved in developing and/or utilizing AI/ML models, fostering enhanced collaboration and integration across the ecosystem.


The CLI enables the deployment of various modules, organized into three main categories based on their functionality: Components, Stages, and Links. These modules are outlined below:

- Components: These refer to advanced frameworks, mainly open-source, designed to address specific tasks within particular domains. These frameworks are essential for improving the performance and scalability of MLOps workflows. The CLI includes the following components:

- Storage: Tools for managing data storage in workflows. Examples include databases such as TimescaleDB and PostgreSQL, as well as MinIO and time-series databases like Prometheus, which are used for tracking sustainability metrics.
    - ML Toolkits: Platforms that support the entire lifecycle of ML/AI models, covering tasks such as data preparation, model training, experimentation, versioning, and deployment. The CLI offers commands for deploying Kubeflow.

    - Serving Platforms: Frameworks designed for deploying and managing ML/AI models in production. The CLI includes commands for setting up TorchServe and TensorFlow Serving, which are tailored for serving PyTorch and TensorFlow models, respectively.

    - Energy Measurement Tools: Modules for monitoring energy usage, such as Kepler and Scaphandre. Plans are underway to expand this catalog, including tools for tracking carbon intensity based on location and grouping sustainability metrics by workflow stages. These features enable the assessment of environmental impact as part of the workflow analysis.

    - Observability: Tools for monitoring and visualization, such as Grafana, which provides insights into the evolution of sustainability metrics in multi-stakeholder environments.

- Stages: This category includes modules that offer specific capabilities for different phases of ML/AI model development. Examples include tools for data encryption and anonymization to ensure data privacy in multi-stakeholder workflows, as well as modules for data validation, model training, and testing. Future updates aim to include modules specifically designed for AI/ML-based network service development.

- Links: These modules facilitate the exchange of data, such as datasets or trained models, across different domains (e.g., between software vendors and network operators). They also handle data sharing between components and stages. The CLI supports two Open APIs:

    - The Model Sharing API, which acts as a registry for storing and sharing trained ML models across domains.
    - The Dataset Sharing API, which is designed to store, share, and manage datasets created for training ML/AI models.


## Installation


The user can find in this folder all files needed to build the Command Tool that will deploy helm charts stored in install/k8s folder located in this repository.

This project is build over Python 3.12.3. You need to have this python version installed in your laptop. Execute the following command to build an environment:

    $ python  -m venv ./venv (or python3 -m venv ./venv) 
    $ source venv/bin/activate
    (venv) $ --> here your python environment is ready

Install the project dependencies with the following commmand:
    $ pip install -r requirements.txt 

