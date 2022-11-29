FROM cern/cs9-base:latest

LABEL description="CERN CentOS 9 with Acts dependencies from LCG 102 using GCC 11"
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
ENV LCG_RELEASE 102b
ENV LCG_PLATFORM x86_64-centos9-gcc11-opt
COPY lcg.repo /etc/yum.repos.d/

RUN dnf install -y https://linuxsoft.cern.ch/wlcg/el9/x86_64/wlcg-repo-1.0.0-1.el9.noarch.rpm \
  && dnf install -y HEP_OSlibs \
  && dnf install -y \
    LCG_${LCG_RELEASE}_Boost_1.78.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_CMake_3.20.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ROOT_6.26.08_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_DD4hep_01.23_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_EDM4hep_00.04.01_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_podio_00.14.01_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_eigen_3.3.7_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_Geant4_11.0.3_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_hepmc3_3.2.4p1_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ninja_1.10.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_pythia8_307p1_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_tbb_2020_U2_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ccache_4.3_${LCG_PLATFORM//-/_}.noarch \
  && dnf -y clean all

# Create the LCG view.
#
# Use a fixed location since there is only one release/platform combination.
# This way, images with different configurations (including different
# compilers) can be easily substituted without needing to know the specific
# contents.
#
# Make the gcc version installed by LCG findable by the script
RUN ln --relative --symbolic /opt/lcg/gcc/11.3.0 /opt/lcg/gcc/11
RUN git clone https://gitlab.cern.ch/sft/lcgcmake.git lcgcmake \
  && (cd lcgcmake; git checkout master) \
  && lcgcmake/cmake/scripts/create_lcg_view.py \
    --verbose \
    --lcgpath=/opt/lcg/LCG_${LCG_RELEASE} \
    --release=${LCG_RELEASE} \
    --platform=${LCG_PLATFORM} \
    /opt/lcg_view \
  && rm -rf lcgcmake
