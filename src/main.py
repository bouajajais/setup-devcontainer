import sys
from config import init_config
from devcontainer import setup_devcontainer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        init_config()
    else:
        import extensions_configurations # to register configurations and extension configurations
        setup_devcontainer()
    
if __name__ == "__main__":
    main()