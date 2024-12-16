from pyhelm3 import Client
import os
import yaml
from mlopsTool import __library__


async def list_deployed_releases(context: str):
    """Function in charge of listing the deployed releases

    Args:
        context (str): Domain where release is deployed

    Returns:
        _type_: _description_
    """
    
    client = Client(kubecontext = context)
    
    # List the deployed releases
    releases = await client.list_releases(all = True, all_namespaces = True)
    results = []
    for release in releases:
        revision = await release.current_revision()
        ob = {
            "release_name" : release.name,
            "release_namespace": release.namespace,
            "revision": revision.revision,
            "status": str(revision.status)
        }
        results.append(ob)
        
    return results



async def install_or_upgrade_release(
    context: str,
    release_name: str,
    values_path: str):
    """Function in charge of install or upgrade a helm release

    Args:
        context (str):  Domain where release is deployed
        release_name (str):  Name of the release
    """
    
    client = Client(kubecontext = context)
    
    workDir = os.getcwd()
    module_path = os.path.join(workDir, __library__, release_name)
    
    if values_path:
        with open(values_path) as stream:
            file = yaml.safe_load(stream)
    else:
        file = None

    chart = await client.get_chart(chart_ref=module_path)
    revision = await client.install_or_upgrade_release(
            release_name,
            chart,
            file
    )
    
async def delete_release(context: str, release_name: str):
    """Function in charge of deleting a helm release

    Args:
        context (str): Domain where release is deployed
        release_name (str): Name of the release
    """
    
    client = Client(kubecontext = context)
    
    await client.uninstall_release(release_name, wait = True)
    
    
async def get_status(context: str, release_name: str):
    """
    Args:
        context (str): _description_
        release_name (str): _description_
    """
    
    client = Client(kubecontext = context)
    revision  = await client.get_current_revision(release_name)
    
    return {
        "release": revision.release,
        "status": revision.status,
        "updated": revision.updated.strftime("%m/%d/%Y-%H:%M:%S")}
    
    
async def get_info(
    context: str,
    release_name: str,
    values_path: str):
    """
    Args:
        context (str): _description_
        release_name (str): _description_
    """
    
    client = Client(kubecontext = context)
    
    workDir = os.getcwd()
    module_path = os.path.join(workDir, __library__, release_name)
    
    if values_path:
        with open(values_path) as stream:
            file = yaml.safe_load(stream)
    else:
        file = None

    chart = await client.get_chart(chart_ref=module_path)
    template = await client.template_resources(chart, release_name)
    
    
    print(template)