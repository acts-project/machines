FROM gitlab-registry.cern.ch/acts/machines/cc7

LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"

RUN yum -y update \
    && yum -y install \
         llvm-toolset-7-clang-tools-extra \
         llvm-toolset-7-clang \
         python34 \
         python34-pip \
         PyYAML \
    && yum -y clean all

ENV PATH="/opt/rh/llvm-toolset-7/root/usr/bin/:${PATH}"

RUN curl -o /usr/local/bin/run-clang-tidy.py https://raw.githubusercontent.com/llvm-mirror/clang-tools-extra/master/clang-tidy/tool/run-clang-tidy.py \
    && chmod +x /usr/local/bin/run-clang-tidy.py

RUN pip3.4 install virtualenv

