from typing import Optional
from mlopsTool import ERRORS, __app_name__, __version__
from mlopsTool.core.configFile import configFile
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.pretty import pprint

import typer

app = typer.Typer()

@app.callback()
def init():
    """
    Command in charge of configuring the different domains (Software Vendor Domains and MNOs)
    """

@app.command("set_default_domain")
def set_default_domain():
    """ It allow users to configure the default domain to which changes will be applied """
    cf = configFile.get_config_file()
    domains = configFile.get_not_none_domains(cf)
    if cf:
        default_context = inquirer.select(
            message="Select a default domain:",
            choices=domains,
            default=None,
        ).execute()
    else:
        typer.secho(
            f'No configured contexts. Please execute {__app_name__} init new_config',
            fg=typer.colors.YELLOW,
        )

        
    configFile.change_default_domain(default_context)
    

@app.command("show_config")
def show_config():
    """ Displays the application's configuration """

    f = configFile.get_config_file()

    typer.secho(
        "Config file: \n",
        fg=typer.colors.GREEN,
    )
    pprint(f)


@app.command("new_config")
def new_config():
    """ Allows to match each domain (SWVs and MNOs) with its cluster  """

    contexts = configFile.get_kubernetes_contexts()

    if contexts:
        choices = contexts + [Choice(value=None, name="Empty")]
        swv_context = inquirer.select(
        message="Software Vendor domain:",
        choices=choices,
        default=None,
        ).execute()

        if swv_context in choices:
            choices.remove(swv_context)
        mno_staging_context = inquirer.select(
        message="Mobile Network Operator staging domain:",
        choices=choices,
        default=None,
        ).execute()

        if mno_staging_context in choices:
            choices.remove(mno_staging_context)
        mno_production_context = inquirer.select(
        message="Mobile Network Operator production domain:",
        choices=choices,
        default=None,
        ).execute()
        
        app_init_error = configFile.init_app(
        swv_context,
        mno_staging_context,
        mno_production_context)
    
        if app_init_error:
            typer.secho(
                f'Creating config file failed with "{ERRORS[app_init_error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        
        config_file = configFile.get_config_file()
        domains = configFile.get_not_none_domains(config_file)

        if domains:
            default_context = inquirer.select(
                message="Select a default domain:",
                choices=domains,
                ).execute()
        else:
            typer.secho(
                f'Please. at least set one domain.',
                fg=typer.colors.YELLOW,
            )

    else:
        typer.secho(
            f'There are not contexts configurated in kubeconfig file. Please, \
            Configure access to a kubernetes cluster at least',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)