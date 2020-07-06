ARG REGISTRY=gitlab-registry.cern.ch/acts/machines
ARG TAG=latest
FROM ${REGISTRY}/slc6:${TAG}

LABEL description="Scientific Linux CERN 6 with Acts dependencies from LCG 95apython3"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="2"

ENV LCG_RELEASE 95apython3
ENV LCG_PLATFORM x86_64-slc6-gcc8-opt

# Add the LCG rpm repository as described here
#
#     https://lcgpackages.web.cern.ch
#
# and use it to install all explicit Acts dependencies from an LCG release.
RUN yum-config-manager --add-repo https://lcgpackages.web.cern.ch/lcgpackages/rpms/etc/yum.repos.d/lcg.repo \
  && yum -y install \
    LCG_${LCG_RELEASE}_Boost_1.69.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_CMake_3.11.1_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_cmaketools_1.8_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_DD4hep_01_10_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_eigen_3.3.7_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_Geant4_10.05_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_lcgenv_1.3.8_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ninja_1.7.2.gcc0ea.kitware.dyndep_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_pythia8_240_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ROOT_6.16.00_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_tbb_2019_U1_${LCG_PLATFORM//-/_}.noarch \
  && yum -y clean all

# Create the LCG view. Use a fixed location since there is only one
# release/platform combination. This way, images with different
# configurations (including different compilers) can be easily substituted
# without needing to know the specific contents.
RUN git clone https://gitlab.cern.ch/sft/lcgcmake.git lcgcmake \
  && lcgcmake/cmake/scripts/create_lcg_view.py \
    -l /opt/lcg \
    -r ${LCG_RELEASE} \
    -p ${LCG_PLATFORM} \
    /opt/lcg_view \
  && rm -rf lcgcmake
