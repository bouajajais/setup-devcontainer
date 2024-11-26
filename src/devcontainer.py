from functools import wraps
import os
from config import get_config
import settings
from utilities import remove, copy

configurations = []

def register_configuration(configuration):
    @wraps(configuration)
    def wrapper(func):
        configurations.append(configuration)
        return func
    return wrapper

def setup_devcontainer(
    target_folder: str = settings.TARGET_FOLDER,
    template_folder: str = settings.TEMPLATE_FOLDER,
    config: dict = None
    ) -> None:
    if config is None:
        config = get_config()
        
    # Clear folder
    clear_folder = config.get(
        "clear-folder",
        settings.DEFAULT_CONFIG["clear-folder"]
    )
    if clear_folder:
        remove(target_folder)
        os.makedirs(target_folder, exist_ok=True)
        
    # Copy template into target
    copy(template_folder, target_folder)
    
    # Apply configurations
    for configuration in configurations:
        configuration(target_folder, config)