# setup-devcontainer

This Docker image enables easy setup of a Docker devcontainer environment for VSCode. It provides seamless integration between your local development environment and the container, allowing you to leverage VSCode's features and extensions within the containerized environment.

## Available tags

Only `latest` tag is available for now.

Other tags will be added later for proper versioning.

## Usage

### [Optional] Step 1: Pull and edit `config.json`

1. Run the following command to pull the default `config.json` locally:
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /path/to/config.json:/app/config/config.json ismailbouajaja/setup-devcontainer config
    ```

    Here's the default `config.json`:
    ```json
    {
        "clear-folder": true,
        "name": "base-devcontainer",
        "ports": [],
        "include-gpu": true,
        "include-gitignore": true,
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
            "docker": true,
            "copilot": true,
            "python": false
        }
    }
    ```

2. Edit the `config.json` to your liking.

    Here's an example of a `config.json` file:
    ```json
    {
        "clear-folder": true,
        "name": "NAME_OF_IMAGE",
        "ports": [
            "8000:8000"
        ],
        "include-gpu": true,
        "include-gitignore": true,
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
            "docker": true,
            "copilot": true,
            "python": false
        }
    }
    ```

### Step 2: Initialize your project

3. Run the following command :

    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /optional/path/to/config.json:/app/config/config.json -v /path/to/project/folder:/app/data/target ismailbouajaja/setup-devcontainer
    ```

    This will initialize a project in `/path/to/project/folder`.

4. Customize your environment:

    You can start to customize the dev container environment by customizing the generated `Dockerfile.dev`, `compose.dev.yaml` and `.devcontainer/devcontainer.json`.
    
    You can also change `Dockerfile`, `compose.yaml`, `entrypoint.sh` and `set_user_guid.sh` to better fit your project.
    
### Step 3: Start the dev environment

5. Start the dev environment:

    In VS Code, you can `Reopen vscode in container` allowing you and others to develop your project in the right same environment. This feature builds the dev environment using `compose.dev.yaml` then it reopens VS Code inside the container you specify in `.devcontainer/devcontainer.json`.

6. Enjoy programming.

### Step 4: Build and run the image for/by end users

While `Dockerfile`, `compose.yaml` and `.devcontainer/devcontainer.json` are made for the developer(s) to have a proper dev container environment, `Dockerfile`, `compose.yaml`, `entrypoint.sh` and `set_user_guid.sh` are made for end users.

To build and run the end user image, you can either use the `compose.yaml` file or manually build and run the `Dockerfile` yourself. Here are illustrative steps to do so but the actual steps depend on the changes you make to `Dockerfile` and/or `compose.yaml`:

#### Use `compose.yaml` for automated build/run

7. Set `USER_UID` and `USER_GID` variables in `.user_guid.env` using `set_user_guid.sh` script:
    ```bash
    chmod +x ./set_user_guid.sh
    ./set_user_guid.sh
    ```

8. Run `docker compose up --build`
    ```bash
    docker compose up --build
    ```

#### Use `Dockerfile` for manual build/run

7. Build the Docker image using the `Dockerfile`:
    ```bash
    docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t YOUR_IMAGE_NAME .
    ```

8. Run the Docker container:
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) YOUR_IMAGE_NAME
    ```

    While it is only required to provide these environment variables during run time, it is still highly encouraged to build your image with the same arguments `USER_UID` and `USER_GID` to avoid an initial delay when running your container to setup correctly the user's permissions during build time.

    Customize these commands to fit your exact usecase.

## >!! IMPORTANT NOTE !!<

If you set `"clear-folder": true` in your `config.json` file, this will delete the folder and recreate it before initializing the project inside it.

## `config.json` specifications

### - `clear-folder`: `true`

This field can be either `true` or `false` and it defaults to `true`.

Deletes the project's folder and recreates it before populating it.

### - `name`: `"base-devcontainer"`

This field can be any `string` value that respects rules of places where it is used and it defaults to `"base-devcontainers"`.

This `name` is used as the `name` of the devcontainer as well as the docker compose name and service name.

The prefix `dev-` is added to the `name` in `.devcontainer/devcontainer.json` and `compose.dev.yaml` to distinguish the dev environments from the images created using `compose.yaml`.

### - `ports`: `[]`

This field must be an array of exposed ports in the following format `"host_port:container_port"` (for example: `"8000:8000"`) and it defaults to `[]`.

This field populates `.devcontainer/devcontainer.json`'s `"forwardPorts"` and it populates the appropriate fields in `Dockerfile.dev`, `compose.dev.yaml`, `Dockerfile` and `compose.yaml`.

#### NOTE

The ports used in the dev environment and the non-dev environment are the same which blocks having both environments active at the same time unless the ports settings are manually changed.

### - `include-gpu`: `true`

This field can be either `true` or `false` and it defaults to `true`.

This field populates `compose.dev.yaml` and `compose.yaml` to add GPU support inside their corresponding containers. Additional manual verification of these files may be needed to correspond to your exact GPU setup.

### - `include-gitignore`: `true`

This field can be either `true` or `false` and it defaults to `true`.

Whether to copy a pre-filled `.gitignore` into your project.

### - `volumes`

This field is an object with 3 keys:
- `"devcontainer"`
- `"compose"`
- `"devcompose"`

#### -- `devcontainer`: `[]`

This field must be an array of volumes to attach to your dev container when using VS Code `Reopen in container` feature.

#### -- `compose`: (see default `config.json` for default value)

This field must be an array of volumes to attach to the main container of `compose.yaml` built from `Dockerfile`.

It defaults to the following array:
```json
[
    "${DATA_PATH:-./data}:/app/data",
    "${CONFIG_PATH:-./config}:/app/config"
]
```

#### -- `devcompose`: (see default `config.json` for default value)

This field must be an array of volumes to attach to the main dev container of `compose.dev.yaml` built from `Dockerfile.dev`.

It defaults to the following array:
```json
[
    "${DATA_PATH:-./data}:/app/data",
    "${CONFIG_PATH:-./config}:/app/config"
]
```

### - `extensions`

This field is an object that specificies which extensions to add to `.devcontainer/devcontainer.json` for VS Code to automatically install when running inside the dev container. (New extensions will be added with time.)

#### -- `docker`: `true`

This field can be either `true` or `false` and it defaults to `true`.

This installs the `"ms-azuretools.vscode-docker"` VS Code extension in the devcontainer.

#### -- `copilot`: `true`

This field can be either `true` or `false` and it defaults to `true`.

This installs the `"GitHub.copilot"` VS Code extension in the devcontainer.

#### -- `python`: `false`

This field can be either `true` or `false` and it defaults to `true`.

This installs the `"ms-python.python"` VS Code extension in the devcontainer.

It also sets python's interpreter's default path to `${containerEnv:PYTHON_PATH:-/usr/local/bin/python}` which is the environment variable `PYTHON_PATH` defined inside the dev container if it's set, otherwise it's `/usr/local/bin/python`.

A good place to define this environment variable is inside the `Dockerfile`. There's an example for `poetry` users inside the `Dockerfile` template.

## Project Details

### Project structure

This section explains the structure of the project initialized using this image.

- A file `Dockerfile` that defines the image to be built. It includes :
    - A base image
    - Setup for root-user management
    - System-wide setup
    - User-specific setup
    - Default entrypoint that will run entrypoint.sh as root
- A file `compose.yaml` that defines how to build and run the image defined by the `Dockerfile`. It includes :
    - `.user_guid.env` as environment variables file for running the container
    - Other optional elements defined in the `config.json` file such as ports, volumes and gpu declaration
- A file `Dockerfile.dev` that defines the image to be built for the dev environment. It includes :
    - A base image
    - Setup for root-user management
    - System-wide setup
    - User-specific setup
- A file `compose.dev.yaml` that defines how to build and run the image defined by the `Dockerfile.dev`. It includes :
    - Optional elements defined in the `config.json` file such as ports, volumes and gpu declaration
- A file `.devcontainer/devcontainer.json` that defines how the image should be built and run as a development container for VS Code. It includes :
    - `workspaceFolder`: path to the folder to be opened by VS Code inside the dev container
    - `mounts`:
        - mounts current folder (containing `.devcontainer/devcontainer.json`) to the container's `workspaceFolder`
    - `remoteUser` and `containerUser`: Corresponds to the `USERNAME` defined in the `Dockerfile`, to attach to the container as a user instead of the `root` user
    - `overrideCommand`: set to `true`. Keeps the container up and running to be able to attach to it
    - `postStartCommand: "git config --global --add safe.directory ${containerWorkspaceFolder}"`: adds the workspace folder to git safe directories to run git commands within the dev container
    `customizations`: includes `extensions` to be installed automatically within the dev container and `settings` for the container's vs code instance
    - etc.
- `set_user_guid.sh`: to be run first before building the image and running a container using `compose.yaml` and/or `Dockerfile` to set `USER_UID` and `USER_GID` in `.user_guid.env`. This isn't used for the dev environment.
- `entrypoint.sh`: script that is run by default by any container spawned by `docker run` with `Dockerfile` or `docker compose` with `compose.yaml`. It corrects permissions to match the `USER_UID` and `USER_GID` set in `.user_guid.env` within the container before executing command passed to `docker run` command or defined in `compose.yaml` file.
- `src` folder that will contain all the source code of the program
- `config` folder that will contain configuration files and folders
- `data` folder that will contain all data ingested and generated by the program. Depending on the needs of the project, some of `data` will be local to the container, some of it will be mounted as a `named docker volume`, some will be mounted from the host, etc.
- other files such as `.dockerignore`, `.gitignore`

## Clone repository

To clone the github repository, follow these steps :

1. Clone the repository:
    ```bash
    git clone https://github.com/bouajajais/setup-devcontainer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd setup-devcontainer
    ```

### Build and run the Dockerfile
3. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t setup-devcontainer .
    ```

    The `docker build` command accepts the following arguments:
    - `ARG PYTHON_TAG=3.10-slim-buster`: The Python tag to use.
    - `ARG POETRY_VERSION=1.8.*`: The Poetry version to install.

4. Run the Docker container to generate `config.json`:
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /path/to/config.json:/app/data/config/config.json setup-devcontainer config
    ```

5. Run the Docker container to initialize a project:
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /optional/path/to/config.json:/app/data/config/config.json -v /path/to/project/folder:/app/data/target setup-devcontainer
    ```

### Docker compose up

3. Create a `.env` file next to the file `compose.yaml` and define the following environment variables inside :
    ```bash
    CONFIG_FILEPATH=/optional/path/to/config.json
    TARGET_PATH=/path/to/project/folder
    ```

4. Run the following commands :
    ```bash
    chmod +x ./set_user_guid.sh
    ./set_user_guid.sh
    docker compose up --build
    ```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.