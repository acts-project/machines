FROM cern/cc7-base:latest

LABEL maintainer="Moritz Kiehn <msmk@cern.ch>"
LABEL version="1.0"
LABEL description="CERN CentOS 7 with minimal CVMFS dependencies"

# minimal development packages
RUN yum -y update \
    && yum -y install \
        autoconf \
        automake \
        cmake \
        doxygen \
        gcc \
        gcc-c++ \
        gcc-fortran \
        git \
        libtool \
        make \
        patch \
        pkgconfig \
        which \
    && yum -y clean all
# packages needed to run software from cvmfs
RUN yum -y install \
        freeglut-devel \
        libXpm-devel \
        motif-devel \
        redhat-lsb-core \
    && yum -y clean all


RUN curl -SL http://ccl.cse.nd.edu/software/files/cctools-7.0.22-x86_64-centos7.tar.gz \
    | tar -xzC . \
    && rsync -ruv cctools-*/ /usr/local
