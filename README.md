# setup-devcontainer

This Docker image enables easy setup of a Docker devcontainer environment for VSCode. It provides seamless integration between your local development environment and the container, allowing you to leverage VSCode's features and extensions within the containerized environment.

## Available tags

Only `latest` tag is available for now.

Other tags will be added later for proper versioning.

## Usage

To use this image from Docker Hub, run the following command :

```bash
docker run --rm -it \
    -e USER_UID=$(id -u) \
    -e USER_GID=$(id -g) \
    -v /optional/path/to/config.json:/app/data/config/config.json \
    -v /path/to/project/folder:/app/data/target \
    ismailbouajaja/setup-devcontainer
```

This will initialize a project in `/path/to/project/folder`, you can then customize the generated `Dockerfile`, `compose.yaml` and `.devcontainer/devcontainer.json` then `Reopen vscode in container` allowing you and others to develop your project in the right same environment.

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
2. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t setup-devcontainer .
    ```

    The `docker build` command accepts the following arguments:
    - `ARG PYTHON_VERSION=3.12-slim`: The Python version to install.
    - `ARG POETRY_VERSION=1.8`: The Poetry version to install.

3. Run the Docker container:
    ```bash
    docker run --rm -it \
        -e USER_UID=$(id -u) \
        -e USER_GID=$(id -g) \
        -v /optional/path/to/config.json:/app/data/config/config.json \
        -v /path/to/project/folder:/app/data/target \
        setup-devcontainer
    ```

### Docker compose up
2. Create a `.env` file next to the file `compose.yaml` and define the following environment variables inside :
    ```bash
    CONFIG_PATH=/optional/path/to/config.json
    TARGET_PATH=/path/to/project/folder
    ```

3. Run the following commands :
    ```bash
    chmod +x ./set_user_guid.sh
    ./set_user_guid.sh
    docker compose up --build
    ```

### Default config.json

`config.json` file is read by python `json` module and shouldn't have any comments in it.

```json
{
    "clear-folder": false,
    "name": "base-devcontainer",
    "ports": [],
    "include-data": true,
    "data-volumes": {
        "compose": [
            "${DATA_PATH:-./data}:/app/data"
        ],
        "devcontainer": []
    },
    "include-secrets": true,
    "secrets": [],
    "include-gpu": true,
    "git-config": true,
    "include-gitignore": true,
    "include-python": false
}
```

#### IMPORTANT NOTE

If you set `"clear-folder": true` in your `config.json` file, this will delete the folder and recreate it before initializing the project inside it.

## Project Details

### Project structure

This section explains the structure of the project initialized using this image.

- A file `Dockerfile` that defines the image to be built. It includes :
    - A base image
    - System-wide setup
    - User-specific setup
    - Default entrypoint that will run entrypoint.sh as root
- A file `compose.yaml` that defines how to build and run the image defined by the `Dockerfile`. It includes :
    - `USER_UID` and `USER_GID` as build arguments and environment variables for running a container
    - Other optional elements defined in the config.json file such as ports, data volumes, secrets volume, gpu declaration
- A file `.devcontainer/devcontainer.json` that defines how the image should be built and run as a development container for vs code. It includes :
    - `workspaceFolder`: path to the folder opened by vs code within the dev container
    - `mounts`:
        - mounts current folder (containing `.devcontainer/devcontainer.json`) to the container's `workspaceFolder`
        - and mounts `~/.ssh` folder to `/root/.ssh` for services like github from within the dev container
    - `remoteUser`: Corresponds to the `USERNAME` defined in the `Dockerfile`, to attach to the container as a user instead of the `root` user
    - `overrideCommand`: set to `true`. Keeps the container up and running to be able to attach to it
    - `initializeCommand: "chmod +x ./set_user_guid.sh && ./set_user_guid.sh .env"`: sets the `USER_UID` and `USER_GID` environment variables in `.env` to be automatically used by `compose.yaml` for build of the image with the correct user (corresponding to the user of the host)
    - `postStartCommand: "git config --global --add safe.directory ${containerWorkspaceFolder}"`: adds the workspace folder to git safe directories to run git commands within the dev container
    `customizations`: includes `extensions` to be installed automatically within the dev container and `settings` for the container's vs code instance
    - etc.
- `set_user_guid.sh`: to be run first before building the image and running a container to set `USER_UID` and `USER_GID` in `.env`. It is automatically run by vscode when reopening it in container.
- `entrypoint.sh`: script that is run by default by any container spawned by `docker run` or `docker compose`. It corrects permissions within the container before executing command passed to `docker run` command or defined in `compose.yaml` file.
- `code` folder that will contain all the code of the program.
- `data` folder that will contain all data ingested and generated by the program. Depending on the needs of the project, some of `data` will be local to the container, some will be mounted as a `named docker volume`, some will be mounted from the host, etc.
- `secrets` and `.secrets.env` for handling sensitive environment variables :
    - `secrets`: every sensitive environment variable will be stored in one secret file inside this folder (`.openai_api_key` for example)
    - `.secrets.env` will define environment variables that holds the paths to each of the sensitive environment variables in the `secrets` folder. (`OPENAI_KEY_API=/app/secrets/.openai_api_key` for example)
- other files such as `.dockerignore`, `.gitignore`

### Reopen in Container

Once the project is initialized and manually customized to your liking, you can `Reopen in Container` in vscode.

VSCode builds the image then runs a container of that image then attaches the current vscode window to it.

In other words it reopens vscode inside the container.

This allows you to develop within the correct (dev) environment.

The behaviour of these 3 steps is defined in the following files :

- `Dockerfile`: Defines the layers of the image to be built.

- `compose.yaml`: Defines how the image is built and how the container is run. It allows for multiple services to be run.

- `.devcontainer/devcontainer.json`: Customizes the behaviour of `compose.yaml` and defines how vscode attaches itself to the running container.

### Project build and run

You can look up [Docker's documentation](https://docs.docker.com/get-started/) for more custom commands.

In both cases, unless you've updated the original `Dockerfile` and `compose.yaml` global definitions, the environment variables `USER_UID` and `USER_GID` must be provided to the commands below for a correct build/run.

While it is only required to provide these environment variables during run time, it is still highly encouraged to build your image with the same arguments `USER_UID` and `USER_GID` to avoid an initial delay when running your container to setup correctly the user's permissions during build time.

#### Using `docker build` and `docker run`

Using only `Dockerfile`, you can build your image and run a container manually.

Depending on the configuration you've initialized your project with, here is how your `build` and `run` commands would look like :

1. `docker build`:
    ```bash
    docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t put-image-name-here .
    ```

2. `docker run`:
    ```bash
    docker run \
        --gpus all \
        -e USER_UID=$(id -u) \
        -e USER_GID=$(id -g) \
        -v /your/first/mounted/volume:/app/data/first/volume \
        -v /your/second/mounted/volume:/app/data/second/volume \
        --mount type=bind,src=./secrets,dst=/run/secrets,readonly=true \
        --env-file .secrets.env \
        --name put-image-name-here
        put-image-name-here
    ```

#### Using `docker compose`

Using `compose.yaml` alongside `Dockerfile`, you can build your image(s) and run one or multiple containers/services in a more automated and predefined way.

1. Environment variables `USER_UID` and `USER_GID` must be defined with user's ids. One way to do so is to run the `./set_user_guid.sh` script that will define these variables correctly in `.compose.env` file.

```bash
chmod +x ./set_user_guid.sh
./set_user_guid.sh .compose.env
```

Here's how your `compose` command would typically look like :

```bash
docker compose --env-file .compose.env up --build
```

### NOTE : git

For `git` to be available within the dev container, you need to use a base image in the `Dockerfile` that has `git` installed or install it on top of the base image.

Otherwise, you will have to reopen vs code in the host in order to use git.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.