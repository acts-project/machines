Container images for Acts
=========================

Two types of container images are available: images that contain all
dependencies to build the Acts project and images intended for static checks.
The images are intended to be used in the continuous integration pipeline.

The image definitions are usually split: the base image installs only
dependencies available through the system package manager, the derived
images contain all dependencies installed either via a custom built or
through an LCG release.

The `archive` folder contains image definitions that are not actively used.

How to build an image
---------------------

The following command builds an image based on CERN CentOS 7 with dependencies
from LCG release 95apython3

    docker build --pull centos7_lcg95apython3

where `--pull` ensures that the latest version of all base images are used.
This should result in the following output

    ...
    Successfully built <image_hash>

The created image is now usable on your local machine using `<image_hash>` as
the identifier.

