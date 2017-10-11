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
# packages needed to run software from cvmfs
RUN yum -y install \
        freeglut-devel \
        libXpm-devel \
        openmotif-devel \
    && yum -y clean all
# packages for deployment
RUN yum -y install \
        tar \
        krb5-workstation\
    && yum -y clean all
