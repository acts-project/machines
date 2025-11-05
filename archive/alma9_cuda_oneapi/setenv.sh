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
# CERN's Tesla T4 support sm_75
export SYCLCXX="${CXX} -fsycl"
export SYCLFLAGS="-fsycl-targets=nvidia_gpu_sm_75 -Xclang -opaque-pointers -Wno-unknown-cuda-version"

# Set up CUDA.
export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility
export PATH=/usr/local/cuda/bin:"$PATH"
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:"$LD_LIBRARY_PATH"
export CUDAHOSTCXX="clang++"
export CUDAFLAGS="-allow-unsupported-compiler"

# Clean
unset GCCDIR

# For user's convenience:
export TRACCC_URL="https://github.com/acts-project/traccc"
echo "git clone $TRACCC_URL"
echo "cmake -S . -B buildsyclcuda -DTRACCC_BUILD_SYCL=ON -DTRACCC_USE_ROOT=OFF -DCMAKE_INSTALL_PREFIX:PATH=./installed"
echo "cmake --build buildsyclcuda --target install"

echo 'alias ll="ls -lh"' > ~/.bashrc

bash
