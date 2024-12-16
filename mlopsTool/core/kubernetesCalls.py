from kubernetes import client, utils, watch
from kubernetes import config as kubeconfig



def check_connection(context: str) -> str:
    """Kubernetes query to get the status of the cluster

    Args:
        context (str): name of domain to check

    Returns:
        str: {"status": "On" or off, "nodes": nodes or []}
    """
    
    try:
         
        kubeconfig.load_kube_config(context=context)
        v1 = client.CoreV1Api()
         
        api_response = v1.list_node()
        
        nodes = []
        for node in api_response.items:
            nodes.append(node.metadata.name)
            
        return {"status": "On", "nodes": nodes}
    except BaseException as e:
        print(e)
        return {"status": "Off", "nodes": []}




def get_kubernetes_contexts() -> list:
    """Connect to kubernetes to get the kubeconfig contexts

    Returns:
        list: _description_
    """

    try:
        kubeconfig.load_kube_config()
        v1 = client.CoreV1Api()

        contexts, _ = kubeconfig.list_kube_config_contexts()
        context_names = [item["name"] for item in contexts]
        return context_names

    except BaseException:
        return []
    
    

def apply_dir(context: str, yaml_dir) -> list :
    """apply manifiests dirs to kubernetes cluster
    """

    try:
        kubeconfig.load_kube_config(context=context)
        k8s_client = client.ApiClient()

        components = utils.create_from_directory(k8s_client, yaml_dir, verbose=True)

    except BaseException as e:
        print(e)
        return []
    
    
def wait(context: str, label_selector: str,  namespace: str = None, timeout_seconds : int = 60):
    
    
    kubeconfig.load_kube_config(context=context)
    w = watch.Watch()
    core_v1 = client.CoreV1Api()
    for event in w.stream(func=core_v1.list_namespaced_pod,
                            label_selector=label_selector,
                            timeout_seconds=timeout_seconds):
        
        print(event)
        if event["object"].status.phase == "Established":
            w.stop()
            return