FROM ubuntu:18.10

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
  xz-utils \
  curl \
  rsync \
  libtinfo5 \
  git \
  && rm -rf /var/lib/apt/lists/*

# install clang
ENV CLANG_VERSION=8.0.0
RUN curl -SL http://releases.llvm.org/${CLANG_VERSION}/clang+llvm-${CLANG_VERSION}-x86_64-linux-gnu-ubuntu-18.04.tar.xz \
  | tar -xJC . \
  && mv clang+llvm-*-x86_64-linux-gnu-ubuntu-18.04 clang \
  && cp clang/bin/clang-format /usr/local/bin \
  && rm -rf clang
