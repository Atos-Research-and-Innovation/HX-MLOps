import subprocess


def apply_dir(context: str, dir_path: str ):
    
    apply_process = subprocess.run(
        ["kubectl", "apply", "-k", dir_path, "--context", context],   
        check=True,
        )
    
def wait(context: str, condition: str, timeout_seconds: int, label ):

    apply_process = subprocess.run(
        ["kubectl", "wait", "--for", f"condition={condition}", "--context", context, f"--timeout={timeout_seconds}s", label ],   
        check=True,
        )
    
    
def delete_dir(context: str, dir_path: str ):
    
    apply_process = subprocess.run(
        ["kubectl", "delete", "-k", dir_path, "--context", context],   
        check=True,
        )
    
def info_dir(context: str, namespace: str = None):
    
    if namespace:
        apply_process = subprocess.run(
            ["kubectl", "get", "all", "--context", context, "--namespace", namespace],   
            check=True,
            )
    else:
        apply_process = subprocess.run(
            ["kubectl", "get", "all", "--context", context],   
            check=True,
            )