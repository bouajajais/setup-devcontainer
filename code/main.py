import json
import os
import yaml
import shutil

def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def main():
    config_filepath = "/app/data/config/config.json"
    base_folder = "/app/data/base"
    target_folder = "/app/data/target"
    
    # read config file
    with open(config_filepath, "r") as f:
        config = json.load(f)
    
    # clear folder
    clear_folder = config.get("clear-folder", True)
    if clear_folder:
        remove(target_folder)
        os.makedirs(target_folder, exist_ok=True)
    
    # copy Dockerfile template
    shutil.copy(f"{base_folder}/Dockerfile", f"{target_folder}/Dockerfile")
    
    # copy compose.yaml template
    shutil.copy(f"{base_folder}/compose.yaml", f"{target_folder}/compose.yaml")
    
    # copy devcontainer.json template
    os.makedirs(f"{target_folder}/.devcontainer", exist_ok=True)
    shutil.copy(f"{base_folder}/.devcontainer/devcontainer.json", f"{target_folder}/.devcontainer/devcontainer.json")
    
    # copy .dockerignore template
    shutil.copy(f"{base_folder}/.dockerignore", f"{target_folder}/.dockerignore")
    
    # copy set_user_guid.sh template
    shutil.copy(f"{base_folder}/set_user_guid.sh", f"{target_folder}/set_user_guid.sh")
    
    # copy entrypoint.sh template
    shutil.copy(f"{base_folder}/entrypoint.sh", f"{target_folder}/entrypoint.sh")
        
    # create code folder
    os.makedirs(f"{target_folder}/code", exist_ok=True)
    
    ## NAME
    
    name = config.get("name", "base-devcontainer")
    # update .devcontainer/devcontainer.json with project name
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    devcontainer["name"] = name
    devcontainer["service"] = name
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)

    # update compose.yaml with project name
    with open(f"{target_folder}/compose.yaml", "r") as f:
        compose = yaml.safe_load(f)
    compose["name"] = name
    compose["services"][name] = compose["services"]["name_placeholder"]
    del compose["services"]["name_placeholder"]
    compose["services"][name]["image"] = name
    with open(f"{target_folder}/compose.yaml", "w") as f:
        yaml.dump(compose, f)
        
    ## PORTS
        
    ports = config.get("ports", [])
    # update .devcontainer/devcontainer.json with ports
    if len(ports) != 0:
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
            devcontainer = json.load(f)
        devcontainer["forwardPorts"] = ports
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
            json.dump(devcontainer, f, indent=4)
        
    # update compose.yaml with ports
    if len(ports) != 0:
        with open(f"{target_folder}/compose.yaml", "r") as f:
            compose = yaml.safe_load(f)
        compose["services"][name]["ports"] = ports
        with open(f"{target_folder}/compose.yaml", "w") as f:
            yaml.dump(compose, f)
            
    ## DATA
    
    include_data = config.get("include-data", True)
    if include_data:
        os.makedirs(f"{target_folder}/data", exist_ok=True)
    
        ## DATA VOLUMES
        
        data_volumes = config.get("data-volumes", {})
        data_volumes["compose"] = data_volumes.get("compose", ["${DATA_PATH:-./data}:/app/data"])
        data_volumes["devcontainer"] = data_volumes.get("devcontainer", [])
        # update .devcontainer/devcontainer.json with data volumes
        if len(data_volumes["devcontainer"]) != 0:
            with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
                devcontainer = json.load(f)
            current_mounts = devcontainer.get("mounts", [])
            devcontainer["mounts"] = current_mounts + data_volumes["devcontainer"]
            with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
                json.dump(devcontainer, f, indent=4)
        
        # update compose.yaml with data volumes
        if len(data_volumes["compose"]) != 0:
            with open(f"{target_folder}/compose.yaml", "r") as f:
                compose = yaml.safe_load(f)
            current_volumes = compose["services"][name].get("volumes", [])
            compose["services"][name]["volumes"] = current_volumes + data_volumes["compose"]
            with open(f"{target_folder}/compose.yaml", "w") as f:
                yaml.dump(compose, f)
    
    ## SECRETS
    
    include_secrets = config.get("include-secrets", True)
    if include_secrets:
        os.makedirs(f"{target_folder}/secrets", exist_ok=True)
        with open(f"{target_folder}/.secrets.env", "w") as f:
            pass
        
        # update compose.yaml with secrets volume and .secrets.env env_file
        with open(f"{target_folder}/compose.yaml", "r") as f:
            compose = yaml.safe_load(f)
        # volumes
        current_volumes = compose["services"][name].get("volumes", [])
        secrets_volume = {
            "type": "bind",
            "source": "${SECRETS_PATH:-./secrets}",
            "target": "/run/secrets",
            "read_only": True
        }
        compose["services"][name]["volumes"] = current_volumes + [secrets_volume]
        # env_file
        current_env_files = compose["services"][name].get("env_file", [])
        compose["services"][name]["env_file"] = current_env_files + ["${SECRETS_ENV:-.secrets.env}"]
        with open(f"{target_folder}/compose.yaml", "w") as f:
            yaml.dump(compose, f)
                
        ## SECRETS FILES
        
        secrets: list[str] = config.get("secrets", [])
        # update secrets and .secrets.env with secrets files and paths
        for secret in secrets:
            try:
                secret_name, secret_value = secret.split("=")
            except Exception as e:
                secret_name = secret
                secret_value = ""
            secret_path = f"{target_folder}/secrets/.{secret_name.lower()}"
            # create secret file
            with open(secret_path, "w") as f:
                f.write(f"{secret_name.upper()}={secret_value}\n")
            # update .secrets.env with path
            with open(f"{target_folder}/.secrets.env", "w") as f:
                f.write(f"{secret_name.upper()}={secret_path}\n")
        
    ## GPU
    
    include_gpu = config.get("include-gpu", False)
    if include_gpu:
        # update compose.yaml to include gpu
        with open(f"{target_folder}/compose.yaml", "r") as f:
            compose = yaml.safe_load(f)
        compose["services"][name]["deploy"] = {
            "resources": {
                "reservations": {
                    "devices": [
                        {
                            "driver": "nvidia",
                            "capabilities": ["gpu"]
                        }
                    ]
                }
            }
        }
        with open(f"{target_folder}/compose.yaml", "w") as f:
            yaml.dump(compose, f)
    
    ## GIT
        
    git_config = config.get("git-config", True)
    if git_config:
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
            devcontainer = json.load(f)
        devcontainer["postStartCommand"] = {
            "git config": "git config --global --add safe.directory ${containerWorkspaceFolder}"
        }
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
            json.dump(devcontainer, f, indent=4)
            
    ## GITIGNORE
    
    include_gitignore = config.get("include-gitignore", True)
    if include_gitignore:
        shutil.copy(f"{base_folder}/.gitignore", f"{target_folder}/.gitignore")
        
    ## PYTHON
    
    include_python = config.get("include-python", False)
    if include_python:
        # update .devcontainer/devcontainer.json to include python related stuff
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
            devcontainer = json.load(f)
        devcontainer["customizations"]["vscode"] = devcontainer["customizations"].get("vscode", {})
        # add python extension
        devcontainer["customizations"]["vscode"]["extensions"] = devcontainer["customizations"]["vscode"].get("extensions", [])
        if "ms-python.python" not in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].append("ms-python.python")
        # set python path
        devcontainer["customizations"]["vscode"]["settings"] = devcontainer["customizations"]["vscode"].get("settings", {})
        devcontainer["customizations"]["vscode"]["settings"]["python.pythonPath"] = "${containerEnv:PYTHON_PATH:-/usr/local/bin/python}"
        with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
            json.dump(devcontainer, f, indent=4)
        
if __name__ == "__main__":
    main()