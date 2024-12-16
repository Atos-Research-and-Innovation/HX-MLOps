from mlopsTool import ERRORS, __app_name__, __version__
from rich import print as pprint
from mlopsTool.cli.utils.kubectl import create_asset, delete_asset, get_info
from typing_extensions import Annotated
from enum import Enum
from typing import Optional

import typer

app = typer.Typer()


state = {"category": None}

class Modules(str, Enum):
   kubeflowPipeline = "kubeflowPipeline"


@app.callback()
def ml_tookit():
   """
   Allows users to carry out different actions over 'ml_toolkit' modules.
   """

@app.command("create")
def create(
   asset_name: Annotated[Modules, typer.Argument()],
   config_file: Annotated[Optional[str], typer.Option("--file")] = None,
   domain: Annotated[Optional[str], typer.Option("--domain")] = None):
   """Command in charge of deploying the module given as parameter

   Args:
       asset_name (Modules): A module to be deployed
       config_file (str): Path to the config file of the module [OPTIONAL]. Default: None.
   """
   create_asset(asset_name, config_file, domain)
   
   
@app.command("delete")
def delete(
   asset_name: Annotated[Modules, typer.Argument()],
   config_file: Annotated[Optional[str], typer.Option("--file")] = None,
   domain: Annotated[Optional[str], typer.Option("--domain")] = None):
   """Command in charge of deleting the module given as parameter

   Args:
       asset_name (Modules): A module to be deleted
       config_file (str): Path to the config file of the module.
   """
   print(f"deleting {asset_name} module")
   delete_asset(asset_name, config_file, domain)
   
   
@app.command("info")
def info(
   asset_name: Annotated[Modules, typer.Argument()],
   domain: Annotated[Optional[str], typer.Option("--domain")] = None):
   """Command in charge of showing information regarding the asset_name given as parameter:
         - kubeflowPipeline : Give infornation above the differents modules deployed

   Args:
       asset_name (Modules): A module to get the info.
   """
   print(f"giving info about {asset_name}")
   get_info(asset_name, domain)