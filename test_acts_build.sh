#!/bin/bash
set -e

image=$1

echo "Image is $1"


command=$(tr -d "\n" <<-END
	git clone https://github.com/acts-project/acts.git . 
	&& mkdir build
	&& source /opt/lcg_view/setup.sh
	&& cmake -GNinja -S . -B build -DACTS_BUILD_EVERYTHING=ON -DACTS_BUILD_EXAMPLES_PYTHON_BINDINGS=ON -DCMAKE_CXX_STANDARD=17
	&& cmake --build build
END
)

docker run --rm -w /src $image bash -c "$command"
