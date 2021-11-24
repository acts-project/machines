FROM cern/c8-base:latest

LABEL description="CERN CentOS 8 with Acts dependencies from LCG 100 using GCC 10"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# Install all LCG dependencies from the system package manager by using the
# HEP_OSlibs metapackage as described here
#
#     https://gitlab.cern.ch/linuxsupport/rpms/HEP_OSlibs
#
# Add the LCG rpm repository as described here
#
#     https://lcgdocs.web.cern.ch
#
# and use it to install all explicit Acts dependencies from an LCG release.
ENV LCG_RELEASE 100
ENV LCG_PLATFORM x86_64-centos8-gcc10-opt
ADD lcg.repo /etc/yum.repos.d/

RUN dnf install -y https://linuxsoft.cern.ch/wlcg/centos8/x86_64/wlcg-repo-1.0.0-1.el8.noarch.rpm \
    && dnf install -y HEP_OSlibs \
    && ln -s /usr/bin/python2 /usr/bin/python \
    && dnf -y install \
    LCG_${LCG_RELEASE}_Boost_1.75.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_CMake_3.20.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_DD4hep_01.16.01_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_eigen_3.3.7_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_Geant4_10.07.p01_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_hepmc3_3.2.3_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ninja_1.10.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_pythia8_245_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ROOT_v6.24.00_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_tbb_2020_U2_${LCG_PLATFORM//-/_}.noarch \
  && dnf -y clean all

# Create the LCG view.
#
# Use a fixed location since there is only one release/platform combination.
# This way, images with different configurations (including different
# compilers) can be easily substituted without needing to know the specific
# contents.
#
# Make the gcc version installed by LCG findable by the script
RUN ln --relative --symbolic /opt/lcg/gcc/10.1.0 /opt/lcg/gcc/10
RUN git clone https://gitlab.cern.ch/sft/lcgcmake.git lcgcmake \
  && (cd lcgcmake; git checkout master) \
  && lcgcmake/cmake/scripts/create_lcg_view.py \
    --verbose \
    --lcgpath=/opt/lcg/LCG_${LCG_RELEASE} \
    --release=${LCG_RELEASE} \
    --platform=${LCG_PLATFORM} \
    /opt/lcg_view \
  && rm -rf lcgcmake

# LCIO sets it's root include path for cmake absolute, remedy this with a symlink
RUN ln -s /opt/lcg/LCIO /LCIO 

RUN /opt/lcg/gcc/10/x86_64-centos8/libexec/gcc/x86_64-pc-linux-gnu/10.1.0/install-tools/mkheaders
