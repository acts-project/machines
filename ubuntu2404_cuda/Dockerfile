# @TODO: Update this
FROM ghcr.io/acts-project/ubuntu2404:53

LABEL description="Ubuntu 24.04 with Acts dependencies and CUDA"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="2"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

RUN curl -SL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb \
       -o cuda-keyring.deb && \
    dpkg -i cuda-keyring.deb && \
    rm cuda-keyring.deb

# Install CUDA.
ARG CUDA_VERSION=12-6
RUN apt-get update && \
    apt-get install -y cuda-compat-${CUDA_VERSION} cuda-cudart-${CUDA_VERSION} \
                       cuda-libraries-dev-${CUDA_VERSION}                      \
                       cuda-command-line-tools-${CUDA_VERSION}                 \
                       cuda-minimal-build-${CUDA_VERSION} &&                   \
    apt-get clean -y

ENV CUDA_PATH "/usr/local/cuda/"
ENV CUDA_ROOT "${CUDA_PATH}"
ENV CUDA_HOME "${CUDA_PATH}"
ENV CUDACXX "${CUDA_PATH}/bin/nvcc"
ENV CUDACC "${CUDA_PATH}/bin/nvcc"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV PATH "${CUDA_PATH}/bin:${PATH}"
ENV LD_LIBRARY_PATH "${CUDA_PATH}/lib64:${LD_LIBRARY_PATH}"
