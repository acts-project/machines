# Build and install dependencies for Acts using ExternalProject.
#
# Assumes an Ubuntu system and builds only HEP-specific dependencies
# that are usually not available through the system package manager.
cmake_minimum_required(VERSION 3.13)

project(ActsDependencies LANGUAGES C CXX)

# check for packages expected to be already installed.
#
# do not check for versions to avoid inconsistencies with the requirements
# in the Acts repository itself.
find_package(Boost REQUIRED COMPONENTS filesystem program_options unit_test_framework)
find_package(Doxygen REQUIRED)
find_package(Eigen3 REQUIRED)
# TBB should be available, but does not provde a CMake config

# build and install HEP-specific packages
set(DD4hep_VERSION 01-12-01)
set(DD4hep_CHECKSUM SHA256=85e8c775ec03c499ce10911e228342e757c81ce9ef2a9195cb253b85175a2e93)
set(HepMC3_VERSION 3.2.1)
set(HepMC3_CHECKSUM SHA256=6e4e4bb5708af105d4bf74efc2745e6efe704e942d46a8042f7dcae37a4739fe)
set(Geant4_VERSION 10.06.p01)
set(Geant4_CHECKSUM SHA256=73459f823a20cc21ec58da491cc464aaeb771ea560f9e6c692b4efd3da795d6b)
set(Pythia8_VERSION 8244)
set(Pythia8_CHECKSUM SHA256=e34880f999daf19cdd893a187123927ba77d1bf851e30f6ea9ec89591f4c92ca)
set(ROOT_VERSION 6.20.04)
set(ROOT_CHECKSUM SHA256=1f8c76ccdb550e64e6ddb092b4a7e9d0a10655ef80044828cba12d5e7c874472)

# simplify options for cmake-based packages
set(
  COMMON_CMAKE_ARGS
  -DCMAKE_BUILD_TYPE=Release
  -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
  -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
  -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
  -DCMAKE_PREFIX_PATH=${CMAKE_INSTALL_PREFIX}
)

include(ExternalProject)
ExternalProject_Add(
  Geant4
  URL https://geant4-data.web.cern.ch/geant4-data/releases/geant4.${Geant4_VERSION}.tar.gz
  URL_HASH ${Geant4_CHECKSUM}
  CMAKE_ARGS
    ${COMMON_CMAKE_ARGS}
    -DGEANT4_BUILD_CXXSTD=17
    -DGEANT4_INSTALL_DATA=OFF
    -DGEANT4_USE_GDML=ON
    -DGEANT4_USE_SYSTEM_EXPAT=ON
    -DGEANT4_USE_SYSTEM_ZLIB=ON
)
ExternalProject_Add(
  ROOT
  URL https://root.cern/download/root_v${ROOT_VERSION}.source.tar.gz
  URL_HASH ${ROOT_CHECKSUM}
  CMAKE_ARGS
    ${COMMON_CMAKE_ARGS}
    -DCMAKE_CXX_STANDARD=17
    -Dcxx11=OFF
    -Dcxx14=OFF
    -Dcxx17=ON
    -Dgdml=ON
)
ExternalProject_Add(
  DD4hep
  DEPENDS Geant4
  URL https://github.com/AIDASoft/DD4hep/archive/v${DD4hep_VERSION}.tar.gz
  URL_HASH ${DD4hep_CHECKSUM}
  CMAKE_ARGS
    ${COMMON_CMAKE_ARGS}
    -DCMAKE_CXX_STANDARD=17
    -DBUILD_TESTING=OFF
    -DDD4HEP_IGNORE_GEANT4_TLS=ON
    -DDD4HEP_USE_GEANT4=ON
    -DDD4HEP_USE_XERCESC=ON
)
ExternalProject_Add(
  HepMC3
  URL https://hepmc.web.cern.ch/hepmc/releases/HepMC3-${HepMC3_VERSION}.tar.gz
  URL_HASH ${HepMC3_CHECKSUM}
  CMAKE_ARGS
    ${COMMON_CMAKE_ARGS}
    -DHEPMC3_BUILD_STATIC_LIBS=OFF
    -DHEPMC3_ENABLE_PYTHON=OFF
    -DHEPMC3_ENABLE_ROOTIO=OFF
    -DHEPMC3_ENABLE_SEARCH=OFF
)
ExternalProject_Add(
  Pythia8
  DEPENDS HepMC3
  URL http://home.thep.lu.se/~torbjorn/pythia8/pythia${Pythia8_VERSION}.tgz  
  URL_HASH ${Pythia8_CHECKSUM}
  CONFIGURE_COMMAND 
    ./configure
    --cxx=${CMAKE_CXX_COMPILER}
    --enable-shared
    --with-hepmc3=${CMAKE_INSTALL_PREFIX}
  BUILD_COMMAND make
  BUILD_IN_SOURCE TRUE
  INSTALL_COMMAND make install
)

