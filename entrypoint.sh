#!/bin/sh

## This script is used to change the UID and GID of the user running the container
## to match the UID and GID of the user on the host machine. This is done to avoid
## permission issues when mounting volumes from the host machine to the container.
## This script must be run as the root user.

# USERNAME of the default user created during the image build
USERNAME=user

# WORKDIR
WORKDIR=/app

# Exit if not connected as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Define the USER_UID and USER_GID environment variables instead."
    exit 1
fi

# Exit if the UID and GID are not provided
if [ -z "${USER_UID}" ] || [ -z "${USER_GID}" ]; then
    echo "USER_UID and USER_GID environment variables must be set."
    exit 1
fi

# Check if the selected user does NOT correspond to the default user
if [ "$(id -u ${USERNAME})" -ne "${USER_UID}" ] || [ "$(id -g ${USERNAME})" -ne "${USER_GID}" ]; then
    # Change ownership of the home directory and application directory
    chown -R ${USER_UID}:${USER_GID} /home/${USERNAME} ${WORKDIR}

    # Change the UID and GID of the user if they are different from the default
    if [ "$(id -g ${USERNAME})" -ne "${USER_GID}" ]; then
        groupmod -g ${USER_GID} ${USERNAME}
    fi

    if [ "$(id -u ${USERNAME})" -ne "${USER_UID}" ]; then
        usermod -u ${USER_UID} ${USERNAME}
    fi
fi

# Change the ownership of the application directory
chown -R ${USERNAME}:${USERNAME} ${WORKDIR}

# Run the command as the selected user
# If the command is "config" run "python main.py config"
if [ "$@" = "config" ]; then
    exec gosu ${USERNAME} python main.py config
else
    exec gosu ${USERNAME} "$@"
fi