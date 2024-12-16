from mlopsTool import ERRORS, __app_name__, __version__
from rich import print as pprint
from rich.progress import Progress, SpinnerColumn, TextColumn

import mlopsTool.core.helm3Calls as helm3calls
import mlopsTool.core.configFile.configFile as configFile
import asyncio
import typer


def create_asset(asset_name: str, config_file: str, domain: str):
    
    if domain:
        default_domain = domain
    else:
        default_domain = configFile.get_default_domain()
    
    if default_domain:

        default_context = configFile.get_contextName(default_domain)
        
        if default_context:
            
            confirm = typer.confirm(f"Changes will be applied to {default_domain}:{default_context} domain. Are you sure?")
            
            if confirm:
                with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                ) as progress:
                    progress.add_task(description=f" Creating {asset_name} module", total=None)

                    try:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(helm3calls.install_or_upgrade_release(default_context, asset_name, config_file))
                        loop.close()
                        print("Module created!")
                    except BaseException as e:
                        print(e)
            
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
        
            
            
def delete_asset(asset_name: str, domain: str):
    
    if domain:
        default_domain = domain
    else:
        default_domain = configFile.get_default_domain()
    
    if default_domain:
        default_context = configFile.get_contextName(default_domain)
        
        if default_context:
            
            confirm = typer.confirm(f"Changes will be applied to {default_domain}:{default_context} domain. Are you sure?")
            
            if confirm:
    
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description=f" Deleting {asset_name} module", total=None)
                
                    try:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(helm3calls.delete_release(default_context, asset_name))
                        loop.close()
                    except Exception  as e:
                        print(e)
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
        
         
def get_revision(asset_name: str, domain: str):
    
    if domain:
        default_domain = domain
    else:
        default_domain = configFile.get_default_domain()
        
    if default_domain:
        default_context = configFile.get_contextName(default_domain)
        
        if default_context:
    
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description=f" Revision of {asset_name} module", total=None)
            
                try:
                    loop = asyncio.get_event_loop()
                    revision = loop.run_until_complete(helm3calls.get_status(default_context, asset_name))
                    print(revision)
                    loop.close()
                except Exception  as e:
                    print(e)
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
         
         
def get_info(asset_name, config_file: str):
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
      progress.add_task(description=f" Revision of {asset_name} module", total=None)
   
      try:
         loop = asyncio.get_event_loop()
         revision = loop.run_until_complete(helm3calls.get_info("kind-swv", asset_name, config_file))
         print(revision)
         loop.close()
      except Exception  as e:
         print(e)
    