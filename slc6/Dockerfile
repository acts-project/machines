FROM cern/slc6-base:latest

LABEL maintainer="Moritz Kiehn <msmk@cern.ch>"
LABEL version="1.0"
LABEL description="Scientific Linux CERN 6 with minimal CVMFS dependencies"

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
# packages needed to run software from cvmfs and to deploy a tag
RUN yum -y install \
        freeglut-devel \
        libXpm-devel \
        openmotif-devel \
        tar \
        krb5-workstation\
        redhat-lsb-core \
    && yum -y clean all
