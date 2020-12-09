if [[ -n "$BASH" ]]; then
    SCRIPT_DIR=$BASH_SOURCE[0]
else # assume that zsh
    SCRIPT_DIR=${(%):-%x}
fi

BASE=$(dirname $(readlink -f $SCRIPT_DIR))
PLATFORM=x86_64-centos7



# Source dependencies
BASE_STACK="${BASE} ${BASE_STACK}" # Add element to stack

depends=$BASE/../../../binutils/2.30/$PLATFORM/setup.sh
dependshash=$BASE/../../../binutils/2.30-e5b21/$PLATFORM/setup.sh
if [[ -e "$dependshash" ]]; then
    source $dependshash
elif [[ -e "$depends" ]]; then
    source $depends
else
    echo Could not find setup.sh file for package binutils 
fi
BASE=$(echo $BASE_STACK | cut -f1 -d' ' ) # Restore BASE 

BASE_STACK=$(echo $BASE_STACK | cut -f2- -d' ') # Remove last element from stack

__PKG_NAME=gcc
__PKG_VERSION=8.2.0
__PKG_HASH=3fa06

# Export environmental variables
export PATH=$BASE/bin:$PATH
export MANPATH=$BASE/share/man:$MANPATH

if [ -e "${BASE}/lib64" ]; then
    # Add lib64 if exists
    export LD_LIBRARY_PATH="$BASE/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
if [ -e "${BASE}/lib" ]; then
    # Add lib if exists
    export LD_LIBRARY_PATH="$BASE/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

# Export package specific environmental variables

# see https://gcc.gnu.org/onlinedocs/gcc/Environment-Variables.html
export COMPILER_PATH="${BASE}/libexec/gcc/x86_64-pc-linux-gnu/${__PKG_VERSION}-${__PKG_HASH}"
export LIBRARY_PATH="${BASE}/lib/gcc/x86_64-pc-linux-gnu/${__PKG_VERSION}-${__PKG_HASH}${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH}"
export CPLUS_INCLUDE_PATH="${BASE}/include/c++/${__PKG_VERSION}-${__PKG_HASH}:${BASE}/include/c++/${__PKG_VERSION}-${__PKG_HASH}/x86_64-pc-linux-gnu:${BASE}/lib/gcc/x86_64-pc-linux-gnu/${__PKG_VERSION}-${__PKG_HASH}/include:${BASE}/lib/gcc/x86_64-pc-linux-gnu/${__PKG_VERSION}-${__PKG_HASH}/include-fixed"

export FC=`which gfortran`
export CC=`which gcc`
export CXX=`which g++`
