FROM ghcr.io/acts-project/ubuntu2404:47

LABEL description="Ubuntu 24.04 with Acts dependencies and CUDA"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

ENV CUDA_RUNFILE_NAME="cuda_12.5.0_555.42.02_linux.run"
ENV CUDA_INSTALL_PATH="/usr/local/cuda"

RUN apt install wget

RUN wget https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/${CUDA_RUNFILE_NAME} && \
  chmod +x ${CUDA_RUNFILE_NAME} && \
  ./${CUDA_RUNFILE_NAME} --toolkit --silent --installpath=${CUDA_INSTALL_PATH} && \
  rm ${CUDA_RUNFILE_NAME}

ENV CUDA_PATH="${CUDA_INSTALL_PATH}"
ENV CUDA_ROOT="${CUDA_INSTALL_PATH}"
ENV CUDA_HOME="${CUDA_INSTALL_PATH}"
ENV CUDACXX="${CUDA_INSTALL_PATH}/bin/nvcc"
ENV CUDACC="${CUDA_INSTALL_PATH}/bin/nvcc"

ENV PATH="${CUDA_INSTALL_PATH}/bin:${PATH}"
ENV MANPATH="${CUDA_INSTALL_PATH}/share/man:${MANPATH}"
ENV INCLUDE="${CUDA_INSTALL_PATH}/include:${INCLUDE}"
ENV LD_LIBRARY_PATH="${CUDA_INSTALL_PATH}/lib64:${CUDA_INSTALL_PATH}/lib:${LD_LIBRARY_PATH}"
