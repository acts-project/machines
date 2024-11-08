#!/usr/bin/env bash
GCCDIR=/opt/rh/gcc-toolset-13/root

# Set up gcc 13.
source ${GCCDIR}/../enable
# Set up SYCL compiler, including AMD backend.
source /opt/intel/oneapi/setvars.sh --include-intel-llvm

# Set up the compilers to use (with CMake).
export CC="`which clang` --gcc-toolchain=${GCCDIR}"
export CXX="`which clang++` --gcc-toolchain=${GCCDIR}"

# Set up the compiler and its options for SYCL
# gfx90a is the GPU at RAL
export SYCLCXX="${CXX} -fsycl"
export SYCLFLAGS="-fsycl-targets=amd_gpu_gfx90a -Xclang -opaque-pointers"

export TRACCC_URL="https://github.com/acts-project/traccc"

# Clean
unset GCCDIR

echo "git clone $TRACCC_URL"
echo "cmake -S . -B buildamd -DTRACCC_BUILD_SYCL=ON -DTRACCC_USE_ROOT=OFF -DCMAKE_INSTALL_PREFIX:PATH=./installed"
echo "cmake --build buildamd --target install"

bash
