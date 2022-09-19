FROM nvidia/cuda:11.5.1-cudnn8-devel-ubuntu20.04

LABEL description="Ubuntu 20.04 with prerequisites for running the Exa.TrkX training pipeline"
LABEL maintainer="Benjamin Huth <benjamin.huth@ur.de>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

# install dependencies from the package manager
RUN apt-get update -y \
  && apt-get install -y \
    git \
    python3 \
    python3-dev \
    python3-pip \
  && apt-get clean -y
  
# Software for the training
RUN pip3 install torch==1.11.0+cu115 --extra-index-url https://download.pytorch.org/whl/cu115
RUN pip3 install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.11.0+cu115.html
RUN pip3 install traintrack==0.1.5
RUN pip3 install cupy==11.1.0
RUN pip3 install faiss-gpu==1.7.2

ENV TORCH_CUDA_ARCH_LIST="7.5;8.6"
RUN git clone --recursive https://github.com/lxxue/FRNN src \
  && (cd src && git checkout 3e370d8d9073d4e130363faf87d2370598b5fbf2) \
  && (cd src/external/prefix_sum && pip install .) \
  && (cd src && pip install .) \
  && rm -rf src
