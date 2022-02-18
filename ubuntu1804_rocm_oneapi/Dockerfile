#
# Image building the Intel LLVM compiler from scratch, with Intel and AMD
# backend support.
#

# Base the image on the repository's ubuntu1804_rocm configuration.
FROM ghcr.io/acts-project/ubuntu1804_rocm:v18

# Build the Intel DPC++ compiler from source.
ARG LLVM_VERSION=sycl-nightly/20220217
ARG LLVM_SOURCE_DIR=/root/llvm
ARG LLVM_BINARY_DIR=/root/build
RUN git clone https://github.com/intel/llvm.git ${LLVM_SOURCE_DIR} &&          \
    cd ${LLVM_SOURCE_DIR}/ && git checkout ${LLVM_VERSION} &&                  \
    cmake -G Ninja -DCMAKE_BUILD_TYPE=Release                                  \
       -DCMAKE_INSTALL_PREFIX=${PREFIX}                                        \
       -DCMAKE_INSTALL_LIBDIR=lib                                              \
       -DLLVM_TARGETS_TO_BUILD="X86;AMDGPU"                                    \
       -DLLVM_EXTERNAL_PROJECTS="sycl;llvm-spirv;opencl;libdevice;xpti;xptifw" \
       -DLLVM_ENABLE_PROJECTS="clang;compiler-rt;sycl;llvm-spirv;opencl;libdevice;xpti;xptifw;libclc;lld" \
       -DLLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR=${LLVM_SOURCE_DIR}/llvm-spirv     \
       -DLLVM_EXTERNAL_SYCL_SOURCE_DIR=${LLVM_SOURCE_DIR}/sycl                 \
       -DLLVM_EXTERNAL_LIBDEVICE_SOURCE_DIR=${LLVM_SOURCE_DIR}/libdevice       \
       -DLLVM_EXTERNAL_OPENCL_SOURCE_DIR=${LLVM_SOURCE_DIR}/opencl             \
       -DLLVM_EXTERNAL_XPTI_SOURCE_DIR=${LLVM_SOURCE_DIR}/xpti                 \
       -DXPTI_SOURCE_DIR=${LLVM_SOURCE_DIR}/xpti                               \
       -DLLVM_EXTERNAL_XPTIFW_SOURCE_DIR=${LLVM_SOURCE_DIR}/xptifw             \
       -DLIBCLC_TARGETS_TO_BUILD="amdgcn--;amdgcn--amdhsa"                     \
       -DLIBCLC_GENERATE_REMANGLED_VARIANTS=ON -DSYCL_BUILD_PI_HIP=ON          \
       -DSYCL_BUILD_PI_HIP_PLATFORM=AMD -DLLVM_BUILD_TOOLS=ON                  \
       -DSYCL_ENABLE_WERROR=OFF -DSYCL_ENABLE_XPTI_TRACING=ON                  \
       -DLLVM_ENABLE_LLD=OFF -DLLVM_ENABLE_EH=ON -DLLVM_ENABLE_PIC=ON          \
       -DLLVM_ENABLE_RTTI=ON -DOpenCL_INSTALL_KHRONOS_ICD_LOADER=TRUE          \
       -DSYCL_CLANG_EXTRA_FLAGS="-Xsycl-target-backend=amdgcn-amd-amdhsa --offload-arch=gfx803" \
       -S ${LLVM_SOURCE_DIR}/llvm/ -B ${LLVM_BINARY_DIR} &&                    \
    cmake --build ${LLVM_BINARY_DIR} &&                                        \
    cmake --build ${LLVM_BINARY_DIR} --target sycl-toolchain &&                \
    cmake --install ${LLVM_BINARY_DIR} &&                                      \
    rm -rf ${LLVM_SOURCE_DIR} ${LLVM_BINARY_DIR}

# Set up the correct runtime environment for using the compiler(s).
ENV CC=${PREFIX}/bin/clang
ENV CXX=${PREFIX}/bin/clang++
ENV SYCLCXX="${CXX} -fsycl -fsycl-targets=amdgcn-amd-amdhsa -Xsycl-target-backend=amdgcn-amd-amdhsa --offload-arch=gfx803 -Wno-linker-warnings"
