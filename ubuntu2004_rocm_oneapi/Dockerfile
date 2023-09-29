#
# Image building the Intel LLVM compiler from scratch, with Intel and AMD
# backend support.
#

# Base the image on the repository's ubuntu2004_rocm configuration.
FROM ghcr.io/acts-project/ubuntu2004_rocm:v36

# Build the Intel DPC++ compiler from source.
ARG LLVM_VERSION=2022-12
ARG LLVM_SOURCE_DIR=/root/llvm
ARG LLVM_BINARY_DIR=/root/build
RUN git clone https://github.com/intel/llvm.git ${LLVM_SOURCE_DIR} &&          \
    cd ${LLVM_SOURCE_DIR}/ && git checkout ${LLVM_VERSION} &&                  \
    cmake -DCMAKE_BUILD_TYPE=Release                                           \
       -DCMAKE_INSTALL_PREFIX=${PREFIX}                                        \
       -DLLVM_ENABLE_ASSERTIONS=ON -DCMAKE_INSTALL_LIBDIR=lib                  \
       -DLLVM_TARGETS_TO_BUILD="X86;AMDGPU"                                    \
       -DLLVM_EXTERNAL_PROJECTS="sycl;sycl-fusion;llvm-spirv;opencl;libdevice;xpti;xptifw" \
       -DLLVM_ENABLE_PROJECTS="clang;compiler-rt;sycl;sycl-fusion;llvm-spirv;opencl;libdevice;xpti;xptifw;libclc;lld;clang-tools-extra;openmp" \
       -DLLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR=${LLVM_SOURCE_DIR}/llvm-spirv     \
       -DLLVM_EXTERNAL_SYCL_SOURCE_DIR=${LLVM_SOURCE_DIR}/sycl                 \
       -DLLVM_EXTERNAL_SYCL_FUSION_SOURCE_DIR=${LLVM_SOURCE_DIR}/sycl-fusion   \
       -DLLVM_EXTERNAL_LIBDEVICE_SOURCE_DIR=${LLVM_SOURCE_DIR}/libdevice       \
       -DLLVM_EXTERNAL_XPTI_SOURCE_DIR=${LLVM_SOURCE_DIR}/xpti                 \
       -DXPTI_SOURCE_DIR=${LLVM_SOURCE_DIR}/xpti                               \
       -DLLVM_EXTERNAL_XPTIFW_SOURCE_DIR=${LLVM_SOURCE_DIR}/xptifw             \
       -DLIBCLC_TARGETS_TO_BUILD="amdgcn--;amdgcn--amdhsa"                     \
       -DLIBCLC_GENERATE_REMANGLED_VARIANTS=ON                                 \
       -DLLVM_BUILD_TOOLS=ON -DSYCL_ENABLE_WERROR=OFF                          \
       -DSYCL_INCLUDE_TESTS=OFF -DLLVM_ENABLE_DOXYGEN=OFF                      \
       -DLLVM_ENABLE_SPHINX=OFF -DBUILD_SHARED_LIBS=OFF                        \
       -DSYCL_ENABLE_XPTI_TRACING=ON -DLLVM_ENABLE_LLD=OFF                     \
       -DLLVM_ENABLE_PIC=ON -DLLVM_ENABLE_RTTI=ON -DXPTI_ENABLE_WERROR=OFF     \
       -DOpenCL_INSTALL_KHRONOS_ICD_LOADER=TRUE                                \
       -DSYCL_ENABLE_PLUGINS="opencl;level_zero;hip"                           \
       -DSYCL_ENABLE_KERNEL_FUSION=ON                                          \
       -S ${LLVM_SOURCE_DIR}/llvm/ -B ${LLVM_BINARY_DIR} &&                    \
    export MAKEFLAGS=-j`nproc` &&                                              \
    cmake --build ${LLVM_BINARY_DIR} --target intrinsics_gen &&                \
    cmake --build ${LLVM_BINARY_DIR} &&                                        \
    cmake --build ${LLVM_BINARY_DIR} --target sycl-toolchain &&                \
    cmake --install ${LLVM_BINARY_DIR} &&                                      \
    rm -rf ${LLVM_SOURCE_DIR} ${LLVM_BINARY_DIR}

# Set up the correct runtime environment for using the compiler(s).
ENV CC="${PREFIX}/bin/clang"
ENV CXX="${PREFIX}/bin/clang++"
ENV SYCLCXX="${CXX} -fsycl -fsycl-targets=amdgcn-amd-amdhsa -Xsycl-target-backend --offload-arch=gfx803"
