# Use Ubuntu as base image
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install Python 3.12
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv python3.12-dev && \
    apt-get install -y python3-pip

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.12 -

# Set Python 3.12 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Install any dependencies required for Python development
RUN apt-get install -y build-essential

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]
