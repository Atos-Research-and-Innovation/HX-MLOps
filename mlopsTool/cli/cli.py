"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from typing import Optional, Literal
from mlopsTool import ERRORS, __app_name__, __version__
import mlopsTool.cli.commands.check.cli as check_connection_cli
import mlopsTool.cli.commands.init.cli as init_cli
import mlopsTool.cli.commands.component.cli as component_cli
import mlopsTool.cli.commands.link.cli as link_cli

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

import typer

app = typer.Typer()


app.add_typer(init_cli.app, name="init")
app.add_typer(check_connection_cli.app, name="check")
app.add_typer(component_cli.app, name="component")
app.add_typer(link_cli.app, name="link")



def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return