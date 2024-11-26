# syntax=docker/dockerfile:1

# Set the Python TAG to install
ARG PYTHON_TAG=3.10-slim-buster

# Install Poetry and setup final image on top of the CUDA Python image
FROM python:${PYTHON_TAG} AS base

#### Docker Image Setup for root-user management
## Do not alter this section unless you know what you are doing

# Create a non-root user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && apt-get update \
    && apt-get install -y gosu

# Copy the entrypoint script
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

#### End of Docker Image Setup for root-user management

#### System-wide setup
## Put custom System-wide setup here

# # Set the Poetry version to install
# ARG POETRY_VERSION=1.8.*
# ARG PYTHONDONTWRITEBYTECODE=1
# ARG PYTHONUNBUFFERED=1

# # Set environment variables for Python
# ENV POETRY_VERSION=${POETRY_VERSION} \
#     PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE} \
#     PYTHONUNBUFFERED=${PYTHONUNBUFFERED}

# # Install Poetry in non-development mode
# RUN pip install --upgrade pip \
#     && pip install "poetry==${POETRY_VERSION}"

## End of custom System-wide setup
#### End of System-wide setup

# Switch to the ${USERNAME}
USER $USERNAME

#### User-specific setup
## Put custom user-specific setup here

# # Change the working directory to /app/src
# WORKDIR /app/src

# # Copy Poetry files and install dependencies
# COPY --chown=${USERNAME}:${USERNAME} ./pyproject.toml ./poetry.lock* ./

# # Disable virtualenv creation
# RUN poetry config virtualenvs.create false
# USER root
# # Disable virtualenv creation && Install the dependencies
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-root
# USER ${USERNAME}

# Change the working directory to /app
WORKDIR /app

# Copy the directory contents into the container at /app
COPY --chown=${USERNAME}:${USERNAME} ./ ./

## End of custom user-specific setup
#### End of user-specific setup

# Change the working directory to /app
WORKDIR /app/src

# Switch back to the root user to run the entrypoint
USER root

# Set the entrypoint to adjust UID/GID at runtime and execute the command
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# # Set the default command for the container
# CMD ["poetry", "run", "python", "main.py"]