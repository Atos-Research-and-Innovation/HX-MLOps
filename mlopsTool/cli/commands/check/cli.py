from typing import Optional
from mlopsTool import ERRORS, __app_name__, __version__
from mlopsTool.core.configFile import configFile
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich import print as pprint

import mlopsTool.core.kubernetesCalls as kubecalls 
import typer

app = typer.Typer()


@app.callback()
def check():
    """
    Command to check different things about domains.
    """


@app.command("connection")
def check_connection():
    """ Command in charge of checking the connection to the different domains (swv, mno_staging, mno_production).
        Check the connection between the commands tool and each domain.
    """
    
    cf = configFile.get_config_file()
    domains = configFile.get_not_none_domains(cf)
    if cf:
        selected_domain = inquirer.select(
            message="Select domain to check the connection:",
            choices=domains,
            default=None,
        ).execute()
        selected_context = configFile.get_contextName(selected_domain)
        if selected_context:
            response = kubecalls.check_connection(selected_context)
        else:
            pprint("[bold red] Internal error, domain name not exist![/bold red]")
            raise typer.Exit(1)
    
        if response["status"] == "On":
            pprint("[bold green] connection established![/bold green]")
#            print(f"list_of_nodes: {response["nodes"]}")
            
        else:
            pprint("[bold red] connection Refused![/bold red]")
            
    else:
        typer.secho(
            f'No configured contexts. Please execute {__app_name__} init new_config',
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    

    
    
    
