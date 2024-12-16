from mlopsTool import ERRORS, __app_name__, __version__
from rich import print as pprint
from rich.progress import Progress, SpinnerColumn, TextColumn

import mlopsTool.core.configFile.configFile as configFile
import mlopsTool.core.kubectl as kubectl
import mlopsTool.core.helm3Calls as helm3Calls
import typer
import asyncio


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
                       
                       if asset_name == "kubeflowPipeline":
                            PIPELINE_VERSION="2.2.0"
                            kubectl.apply_dir(default_context, f"github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref={PIPELINE_VERSION}")
                            kubectl.wait(default_context, "established", 60, "crd/applications.app.k8s.io")
                            kubectl.apply_dir(default_context, f"github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref={PIPELINE_VERSION}")
                            
                            loop = asyncio.get_event_loop()
                            loop.run_until_complete(helm3Calls.install_or_upgrade_release(default_context, release_name="kubeflowpipeline", values_path=config_file))
                            loop.close()
                            print("Module created!")
                            
                        
                       else:
                           print("Error")
                       
                       
                    except BaseException as e:
                        print(e)
            
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
        
        
def delete_asset(asset_name: str, config_file: str, domain: str):
    
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
                       
                       if asset_name == "kubeflowPipeline":
                            PIPELINE_VERSION="2.2.0"
                            kubectl.delete_dir(default_context, f"github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref={PIPELINE_VERSION}")
                            kubectl.delete_dir(default_context, f"github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref={PIPELINE_VERSION}")
                            
                            loop = asyncio.get_event_loop()
                            loop.run_until_complete(helm3Calls.delete_release(default_context, release_name="kubeflowpipeline"))
                            loop.close()
                            print("Module deleted!")

                        
                       else:
                           print("Error")
                       
                       
                    except BaseException as e:
                        print(e)
            
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
        
    
    
def get_info(asset_name: str, domain: str):
    
    if domain:
        default_domain = domain
    else:
        default_domain = configFile.get_default_domain()
    
    if default_domain:

        default_context = configFile.get_contextName(default_domain)
        
        if default_context:
            
            confirm = typer.confirm(f"Get-info will be applied to {default_domain}:{default_context} domain. Are you sure?")
            
            if confirm:
                with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                ) as progress:
                    progress.add_task(description=f" Getting info from {asset_name} module", total=None)

                    try:
                       
                       if asset_name == "kubeflowPipeline":
                            kubectl.info_dir(default_context, namespace="kubeflow")
                        
                       else:
                           print("Error")
                       
                       
                    except BaseException as e:
                        print(e)
            
        else:
            print("The domain given is not valid")
                    
    else:
        print("Error. the default domain is not configured.")
        