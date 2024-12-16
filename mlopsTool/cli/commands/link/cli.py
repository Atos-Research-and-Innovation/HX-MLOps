"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from typing import Optional, Literal
from mlopsTool import ERRORS, __app_name__, __version__
import mlopsTool.cli.commands.link.api.cli as api_cli
import mlopsTool.cli.commands.link.mqtt.cli as mqtt_cli


from InquirerPy import inquirer
from InquirerPy.base.control import Choice

import typer

app = typer.Typer()


app.add_typer(api_cli.app, name="api")
app.add_typer(mqtt_cli.app, name="mqtt")



@app.callback()
def link():
    """
    Command related to the 'link' section of the tool.
    """