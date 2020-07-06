FROM cern/cc7-base:latest

LABEL description="CERN CentOS 7 with clang-tidy"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

RUN yum -y install \
    llvm-toolset-7-clang-tools-extra \
    llvm-toolset-7-clang \
    python36 \
    python36-pip \
    PyYAML \
  && yum -y clean all \
  && curl -o /usr/local/bin/run-clang-tidy.py https://raw.githubusercontent.com/llvm-mirror/clang-tools-extra/master/clang-tidy/tool/run-clang-tidy.py \
  && chmod +x /usr/local/bin/run-clang-tidy.py \
  && pip3 install --no-cache-dir --upgrade virtualenv pip

ENV PATH="/opt/rh/llvm-toolset-7/root/usr/bin/:${PATH}"
