from typing import Optional
from mlopsTool import ERRORS, __app_name__, __version__
from mlopsTool.core.configFile import configFile
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich import print as pprint
from enum import Enum

import mlopsTool.core.kubernetesCalls as kubecalls 
import typer

app = typer.Typer()


state = {"category": None}

@app.command("create")
def create(asset_name: str, config_file: str):
   print()
   
   
@app.command("delete")
def delete(asset_name: str, config_file: str):
   print()
   
   
@app.command("info")
def info():
   print()
   
   
# @app.callback()
# def main(category: Categories):
#    """
#    Manage components in the awesome CLI app.
#    """
   
#    state["category"] = category