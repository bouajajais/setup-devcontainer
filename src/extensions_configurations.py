import json
from configurations import register_extension_configuration
import settings

@register_extension_configuration
def configure_copilot(target_folder: str, config: dict) -> None:
    copilot = config.get("extensions", {}).get(
        "copilot",
        settings.DEFAULT_CONFIG["extensions"].get(
            "copilot",
            False
        )
    )
    
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    if copilot:
        if "GitHub.copilot" not in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].append("GitHub.copilot")
    else:
        if "GitHub.copilot" in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].remove("GitHub.copilot")
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)
        
@register_extension_configuration
def configure_docker(target_folder: str, config: dict) -> None:
    docker = config.get("extensions", {}).get(
        "docker",
        settings.DEFAULT_CONFIG["extensions"].get(
            "docker",
            False
        )
    )
    
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    if docker:
        if "ms-azuretools.vscode-docker" not in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].append("ms-azuretools.vscode-docker")
    else:
        if "ms-azuretools.vscode-docker" in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].remove("ms-azuretools.vscode-docker")
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)

@register_extension_configuration
def configure_python(target_folder: str, config: dict) -> None:
    python = config.get("extensions", {}).get(
        "python",
        settings.DEFAULT_CONFIG["extensions"].get(
            "python",
            False
        )
    )
    
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "r") as f:
        devcontainer = json.load(f)
    if python:
        if "ms-python.python" not in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].append("ms-python.python")
        devcontainer["customizations"]["vscode"]["settings"]["python.pythonPath"] = "${containerEnv:PYTHON_PATH:-/usr/local/bin/python}"
    else:
        if "ms-python.python" in devcontainer["customizations"]["vscode"]["extensions"]:
            devcontainer["customizations"]["vscode"]["extensions"].remove("ms-python.python")
        if "python.pythonPath" in devcontainer["customizations"]["vscode"]["settings"]:
            del devcontainer["customizations"]["vscode"]["settings"]["python.pythonPath"]
    with open(f"{target_folder}/.devcontainer/devcontainer.json", "w") as f:
        json.dump(devcontainer, f, indent=4)