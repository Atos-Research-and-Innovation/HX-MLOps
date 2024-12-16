"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from mlopsTool import ERRORS, __app_name__, __version__
import mlopsTool.cli.commands.component.storage.cli as storage_cli
import mlopsTool.cli.commands.component.serving_platform.cli as serving_platform_cli
import mlopsTool.cli.commands.component.ml_toolkit.cli as ml_toolkit_cli
import mlopsTool.cli.commands.component.energy_measurement_asset.cli as energy_measurement_asset_cli
import mlopsTool.cli.commands.component.monitoring.cli as monitoring_cli

import typer

app = typer.Typer()


app.add_typer(storage_cli.app, name="storage")
app.add_typer(serving_platform_cli.app, name="serving_platform")
app.add_typer(ml_toolkit_cli.app, name="ml_toolkit")
app.add_typer(energy_measurement_asset_cli.app, name="energy_measurement_asset")
app.add_typer(monitoring_cli.app, name="monitoring")


@app.callback()
def component():
    """
    Command related to the 'component' section of the tool
    """