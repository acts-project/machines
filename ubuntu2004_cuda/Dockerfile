# Docker machinery, part of the ACTS project
#
# (c) 2021-2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

# Start from the (at the time of writing) latest Acts Ubuntu 20.04 image.
FROM ghcr.io/acts-project/ubuntu2004:v43

# Some description for the image.
LABEL description="Ubuntu 20.04 with Acts dependencies and CUDA"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch"

# Add the Ubuntu 20.04 CUDA repository.
RUN curl -SL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb \
       -o cuda-keyring.deb && \
    dpkg -i cuda-keyring.deb && \
    rm cuda-keyring.deb

# Install CUDA.
ARG CUDA_VERSION=12-4
RUN apt-get update && \
    apt-get install -y cuda-compat-${CUDA_VERSION} cuda-cudart-${CUDA_VERSION} \
                       cuda-libraries-${CUDA_VERSION}                          \
                       cuda-command-line-tools-${CUDA_VERSION}                 \
                       cuda-minimal-build-${CUDA_VERSION} &&                   \
    apt-get clean -y

# Set up the CUDA environment.
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
