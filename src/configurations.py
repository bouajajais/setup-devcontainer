from functools import wraps
import json
import yaml
from devcontainer import register_configuration
import settings
from utilities import remove

extensions_configurations = []

def register_extension_configuration(extension_configuration):
    @wraps(extension_configuration)
    def wrapper(*args, **kwargs):
        print(f"Applying extension configuration: {extension_configuration.__name__}")
        return extension_configuration(*args, **kwargs)
    extensions_configurations.append(wrapper)
    return wrapper

@register_configuration
def configure_name(target_folder: str, config: dict) -> None:
    name = config.get(
        "name",
        settings.DEFAULT_CONFIG["name"]
    )
    devname = f"dev-{name}"
    
    # update .devcontainer/devcontainer.json with project name
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    devcontainer["name"] = devname
    devcontainer["service"] = devname
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)

    # update compose.dev.yaml with project name
    with open(f"{target_folder}/compose.dev.yaml", "r") as f:
        compose = yaml.safe_load(f)
    compose["name"] = devname
    compose["services"][devname] = compose["services"]["NAME_PLACEHOLDER"]
    if devname != "NAME_PLACEHOLDER":
        del compose["services"]["NAME_PLACEHOLDER"]
    compose["services"][devname]["image"] = devname
    with open(f"{target_folder}/compose.dev.yaml", "w") as f:
        yaml.dump(compose, f)

    # update compose.yaml with project name
    with open(f"{target_folder}/compose.yaml", "r") as f:
        compose = yaml.safe_load(f)
    compose["name"] = name
    if name != "NAME_PLACEHOLDER":
        compose["services"][name] = compose["services"]["NAME_PLACEHOLDER"]
        del compose["services"]["NAME_PLACEHOLDER"]
    compose["services"][name]["image"] = name
    with open(f"{target_folder}/compose.yaml", "w") as f:
        yaml.dump(compose, f)

@register_configuration
def configure_ports(target_folder: str, config: dict) -> None:
    ports = config.get(
        "ports",
        settings.DEFAULT_CONFIG["ports"]
    )
        
    # update .devcontainer/devcontainer.json with ports
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    if len(ports) != 0:
        devcontainer["forwardPorts"] = ports
    else:
        if "forwardPorts" in devcontainer:
            del devcontainer["forwardPorts"]
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)
    
    # update compose.dev.yaml with ports
    with open(f"{target_folder}/compose.dev.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if len(ports) != 0:
        compose["services"][compose["name"]]["ports"] = ports
    else:
        if "ports" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["ports"]
    with open(f"{target_folder}/compose.dev.yaml", "w") as f:
        yaml.dump(compose, f)
    
    # update compose.yaml with ports
    with open(f"{target_folder}/compose.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if len(ports) != 0:
        compose["services"][compose["name"]]["ports"] = ports
    else:
        if "ports" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["ports"]
    with open(f"{target_folder}/compose.yaml", "w") as f:
        yaml.dump(compose, f)

@register_configuration
def configure_gpu(target_folder: str, config: dict) -> None:
    include_gpu = config.get(
        "include-gpu",
        settings.DEFAULT_CONFIG["include-gpu"]
    )
    
    # update compose.dev.yaml with GPU
    with open(f"{target_folder}/compose.dev.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if include_gpu:
        compose["services"][compose["name"]]["deploy"] = {
            "resources": {
                "reservations": {
                    "devices": [
                        {
                            "capabilities": ["gpu"],
                            "driver": "nvidia",
                            "count": 1
                        }
                    ]
                }
            }
        }
    else:
        if "deploy" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["deploy"]
    with open(f"{target_folder}/compose.dev.yaml", "w") as f:
        yaml.dump(compose, f)
    
    # update compose.yaml with GPU
    with open(f"{target_folder}/compose.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if include_gpu:
        compose["services"][compose["name"]]["deploy"] = {
            "resources": {
                "reservations": {
                    "devices": [
                        {
                            "capabilities": ["gpu"],
                            "driver": "nvidia",
                            "count": 1
                        }
                    ]
                }
            }
        }
    else:
        if "deploy" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["deploy"]
    with open(f"{target_folder}/compose.yaml", "w") as f:
        yaml.dump(compose, f)

@register_configuration
def configure_gitignore(target_folder: str, config: dict) -> None:
    include_gitignore = config.get(
        "include-gitignore",
        settings.DEFAULT_CONFIG["include-gitignore"]
    )
    
    if not include_gitignore:
        remove(f"{target_folder}/.gitignore")

@register_configuration
def configure_volumes(target_folder: str, config: dict) -> None:
    volumes = config.get(
        "volumes",
        settings.DEFAULT_CONFIG["volumes"]
    )
    
    # update .devcontainer/devcontainer.json with volumes
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    if len(volumes.get("devcontainer", [])) != 0:
        current_mounts = devcontainer.get("mounts", [])
        devcontainer["mounts"] = current_mounts + volumes.get("devcontainer", [])
    else:
        if "mounts" in devcontainer:
            del devcontainer["mounts"]
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)
    
    # update compose.dev.yaml with volumes
    with open(f"{target_folder}/compose.dev.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if len(volumes.get("devcompose", [])) != 0:
        compose["services"][compose["name"]]["volumes"] = volumes.get("devcompose", [])
    else:
        if "volumes" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["volumes"]
    with open(f"{target_folder}/compose.dev.yaml", "w") as f:
        yaml.dump(compose, f)
    
    # update compose.yaml with volumes
    with open(f"{target_folder}/compose.yaml", "r") as f:
        compose = yaml.safe_load(f)
    if len(volumes.get("compose", [])) != 0:
        compose["services"][compose["name"]]["volumes"] = volumes.get("compose", [])
    else:
        if "volumes" in compose["services"][compose["name"]]:
            del compose["services"][compose["name"]]["volumes"]
    with open(f"{target_folder}/compose.yaml", "w") as f:
        yaml.dump(compose, f)

@register_configuration
def configure_extensions(target_folder: str, config: dict) -> None:
    for extension_configuration in extensions_configurations:
        extension_configuration(target_folder, config)