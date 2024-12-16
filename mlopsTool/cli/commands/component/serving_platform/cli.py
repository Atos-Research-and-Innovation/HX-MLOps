from typing import Optional
from mlopsTool import ERRORS, __app_name__, __version__

from typing_extensions import Annotated
from enum import Enum
from mlopsTool.cli.utils.helm3 import create_asset, delete_asset, get_revision, get_info

import typer

app = typer.Typer()


class Modules(str, Enum):
   torchserve = "torchserve"
   tfserving = "tfserving"
   
   
@app.callback()
def serving_platform():
    """
    Allows users to carry out different actions over 'serving_platform' modules.
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
   domain: Annotated[Optional[str], typer.Option("--domain")] = None):
   """Command in charge of deleting the module given as parameter

   Args:
       asset_name (Modules): A module to be deleted
       config_file (str): Path to the config file of the module.
   """
   
   delete_asset(asset_name, domain)
   

@app.command("info")
def info(
   asset_name: Annotated[Modules, typer.Argument()],
   config_file: Annotated[Optional[str], typer.Option("--file")] = None):
   """Command in charge of showing information regarding the asset_name given as parameter.
      Both general asset information and the configuration file to be filled in are displayed.
   

   Args:
       asset_name (Modules): A module to get the info.
   """
   get_info(asset_name, config_file)
   
   
@app.command("status")
def status(asset_name: Annotated[Modules, typer.Argument()],
           domain: Annotated[Optional[str], typer.Option("--domain")] = None):
   """Command in charge of showing the status of an asset given as parameter.
   

   Args:
       asset_name (Modules): A module to get the info.
   """
   get_revision(asset_name, domain)
      