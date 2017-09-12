Docker images for ACTS continous integration
============================================

The docker images are designed to run a full LCG release from CVMFS. The
system contains only a minimal set of development packages. The resulting
docker images are to be used in the Gitlab continous integration system
together with the `cvmfs` tag.

How to create and upload an image
---------------------------------

The image for either CERN CentOS7 or Scientific Linux 6 is build using

    docker build --pull <cc7|slc6>

where `--pull` ensures that the latest version of all base images are used.
This should result in the following output

    ...
    Successfully built <image_hash>

The created image is now usable on your local machine using `<image_hash>` as
the identifier. To upload it to the Gitlab container registry you first need
to login

    docker login gitlab-registry.cern.ch

The image needs to tagged to the correct registry path

    docker tag <image_hash> gitlab-registry.cern.ch/acts/machines/<cc7|slc6>

and can then be pushed to the registry itself

    docker push gitlab-registry.cern.ch/acts/machines/<cc7|slc6>
