# Copyright (C) 2002-2020 CERN for the benefit of the ATLAS collaboration
#
# Script setting up the Intel-Clang version of the image.
#

# The directory of this script.
clangThisdir=$(dirname ${BASH_SOURCE[0]})
clangThisdir=$(\cd ${clangThisdir};\pwd)

# Set up the main environment variables.
export PATH=${clangThisdir}/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=${clangThisdir}/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

# Set up the compilers to use (with CMake).
export CC=`which clang`
export CXX=`which clang++`

# Clean up.
unset clangThisdir
