# syntax=docker/dockerfile:1

FROM ubuntu:22.04

#### System-wide setup
## Put custom system-wide setup here
# ...
# ...
## End of custom system-wide setup
#### End of system-wide setup

#### User-specific setup

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

# Create the user and group with the specified UID/GID
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    # Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Install necessary tools for building su-exec
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gcc \
    libc-dev \
    make

# Download, build, and install su-exec
RUN SU_EXEC_VERSION=0.2 \
    && curl -o /usr/local/bin/su-exec.c -L https://raw.githubusercontent.com/ncopa/su-exec/v${SU_EXEC_VERSION}/su-exec.c \
    && gcc -Wall -Werror -O2 /usr/local/bin/su-exec.c -o /usr/local/bin/su-exec \
    && chown root:root /usr/local/bin/su-exec \
    && chmod 0755 /usr/local/bin/su-exec \
    && rm /usr/local/bin/su-exec.c

# Switch to the ${USERNAME}
USER $USERNAME

## Put custom user-specific setup here
# Do not forget to chown the files to the ${USERNAME} user
# Example:
# COPY --chown=${USERNAME}:${USERNAME} source destination
# ...
# ...
## End of custom user-specific setup

# Copy the entrypoint script
COPY --chown=${USERNAME}:${USERNAME} entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

#### End of user-specific setup

# Switch back to the root user to run the entrypoint
USER root

# Expose the port for the container
# EXPOSE 8000

# Set the entrypoint to adjust UID/GID at runtime and execute the command
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Set the default command for the container
CMD ["bash"]