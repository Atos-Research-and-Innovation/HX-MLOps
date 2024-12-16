"""This module provides the config functionality.
    - create/read/modify the configuration files
    - access to kubeconfig file in order to get the installed contexts by user. 

"""
# mlopsTool/config.py

import yaml
from pathlib import Path
from kubernetes import client
from kubernetes import config as kubeconfig

import typer

from mlopsTool import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

CONFIG_FILE_NAME = "config.yaml"
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / CONFIG_FILE_NAME


CONFIG_FILE_DICT = { 
    "domains": {
        "swv": {
            "context_name": None
        },
        "mno_staging": {
            "context_name": None
        },
        "mno_production":  {
            "context_name": None
        },
    },
    "default_domain": "swv"
}

def init_app(
        swv_context: str,
        mno_staging_context: str,
        mno_production_context: str
    ) -> int:
    """Initialize the application."""

    config_code = _init_config_file(
        swv_context,
        mno_staging_context,
        mno_production_context)
    
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_config_file(
        swv_context: str,
        mno_staging_context: str,
        mno_production_context: str,) -> int:
    """Initialization of config file:
        -- create path and file is no exist
        -- update the given domains
    

    Args:
        swv_context (str): context name of swv
        mno_staging_context (str): context name of mno staging context
        mno_production_context (str):context name of mno production context

    Returns:
        int: _description_
    """
    print(CONFIG_DIR_PATH)
    try:
        CONFIG_DIR_PATH.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("error en la prmera", e)
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError as e:
        return FILE_ERROR
    
    try:
        with open(CONFIG_FILE_PATH, 'w',) as f :
            yaml.dump(CONFIG_FILE_DICT, f, sort_keys=False)
    except OSError:
        return FILE_ERROR
    
    try:
        new_config = CONFIG_FILE_DICT
        new_config["domains"]["swv"]["context_name"] = swv_context
        new_config["domains"]["mno_staging"]["context_name"] = mno_staging_context
        new_config["domains"]["mno_production"]["context_name"] = mno_production_context

        with open(CONFIG_FILE_PATH, 'w',) as f :
            yaml.dump(new_config, f, sort_keys=False)
    except OSError:
        return FILE_ERROR

    return SUCCESS

def change_default_domain(default_domain: str) -> int:
    """In charge of reading the "deafault domain" field in config file
        to update the value of it. 

    Args:
        default_domain (str): The new default domain (It must be one of values in domains dict)

    Returns:
        int: Return the response value. 
    """

    try:
        file = get_config_file()

        file["default_domain"] = default_domain

        with open(CONFIG_FILE_PATH, 'w',) as f :
            yaml.dump(file, f, sort_keys=False)
    except OSError:
        return FILE_ERROR
    
    
def get_contextName(domain: str) -> str:
    """Given a domain, search in config file and return the context name

    Args:
        domain (str): domain name in the config file

    Returns:
        str: context name
    """
    try:
        file = get_config_file()
        context = file["domains"][domain]["context_name"]
        return context

    except BaseException:
        return None


def get_kubernetes_contexts() -> list:
    """Connect to kubernetes to get the kubeconfig contexts

    Returns:
        list: _description_
    """

    try:
        kubeconfig.load_kube_config()
        v1 = client.CoreV1Api()

        contexts, _ = kubeconfig.list_kube_config_contexts()
        context_names = [item["name"] for item in contexts]
        return context_names

    except BaseException:
        return []
    
def get_not_none_domains(config_file: dict) -> list:
    """Given a config file, it is searched the domains whose value is not None

    Args:
        config_file (dict): A dict from a configuration file

    Returns:
        list: List of none domains
    """
    choices = []
    for x, y in config_file["domains"].items():
        if y["context_name"] is not None:
            choices.append(x)
    return choices

def get_config_file() -> dict:
    """It is in charge of reading the configuration file

    Returns:
        dict: configuration file as dictionary object
    """
    try:
        with open(CONFIG_FILE_PATH,'r') as f:
            file = yaml.safe_load(f)
        return file
    except OSError:
        return {}
    
def get_default_domain():
    """It return the default domain
    """
    file = get_config_file()

    return file["default_domain"]
