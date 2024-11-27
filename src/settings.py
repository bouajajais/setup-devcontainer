CONFIG_FILEPATH = "/app/config/config.json"
TEMPLATE_FOLDER = "/app/config/template"
TARGET_FOLDER = "/app/data/target"

DEFAULT_CONFIG = {
    "clear-folder": True,
    "dev-only": False,
    "name": "base-devcontainer",
    "ports": [],
    "include-gpu": True,
    "include-gitignore": True,
    "volumes": {
        "devcontainer": [],
        "compose": [
            "${DATA_PATH:-./data}:/app/data",
            "${CONFIG_PATH:-./config}:/app/config"
        ],
        "devcompose": [
            "${DATA_PATH:-./data}:/app/data",
            "${CONFIG_PATH:-./config}:/app/config"
        ]
    },
    "extensions": {
        "docker": True,
        "copilot": True,
        "python": False
    }
}