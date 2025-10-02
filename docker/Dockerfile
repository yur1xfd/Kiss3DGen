# Use official NVIDIA CUDA 12.1 base image
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/app/venv \
    PATH="/app/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Clean up and free space first
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm -f /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/nvidia-ml.list

# Update package lists with minimal approach
RUN apt-get update --allow-insecure-repositories --allow-unauthenticated || true

# Install only essential dependencies in smaller batches
RUN apt-get install -y --allow-unauthenticated --no-install-recommends \
    ca-certificates \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update --allow-insecure-repositories --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    gnupg \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update --allow-insecure-repositories --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    software-properties-common \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fix GPG keys and add Ubuntu repositories
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0x871920D1991BC93C && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0x3B4FE6ACC0B21F32 && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu jammy main universe" && \
    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu jammy-updates main universe" && \
    add-apt-repository -y "deb http://security.ubuntu.com/ubuntu jammy-security main universe" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install system dependencies in batches to save space
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python development headers and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10-dev \
    python3-dev \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    python3.10-venv \
    python3-pip \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3.10 -m venv /app/venv

# Upgrade pip in the virtual environment
RUN pip install -U pip setuptools wheel

# Install PyTorch with CUDA 12.1
RUN pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu121

# Install xformers
RUN pip install xformers==0.0.27.post1

# Install Pytorch3D dependencies
RUN pip install iopath && \
    pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt240/download.html

# Install torch-scatter
RUN pip install torch-scatter -f https://data.pyg.org/whl/torch-2.4.0+cu121.html

# Copy filtered requirements.txt from build context
COPY requirements-docker.txt /tmp/requirements.txt

# Install requirements with --no-deps to avoid conflicts
RUN pip install --no-deps -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

# Copy the custom_diffusers directory
COPY custom_diffusers/ /app/custom_diffusers/

# Install the editable package
RUN pip install -e /app/custom_diffusers

# Clean up pip cache to save space
RUN pip cache purge

# Create a non-root user for security
RUN useradd -m -u 1000 user && \
    chown -R user:user /app
USER user

# Set the default command
CMD ["bash"]