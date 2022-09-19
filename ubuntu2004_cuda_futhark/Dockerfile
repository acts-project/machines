FROM ghcr.io/acts-project/ubuntu2004_cuda:v27

LABEL description="Ubuntu 20.04 with Acts dependencies, CUDA, and Futhark"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"

# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

# Set GPG key for GHCup
ARG GPG_KEY=7784930957807690A66EBDBE3786C5262ECB4A3F
RUN gpg --batch --keyserver keys.openpgp.org --recv-keys $GPG_KEY

# Install GHCup
RUN \
    curl https://downloads.haskell.org/~ghcup/x86_64-linux-ghcup > /usr/local/bin/ghcup && \
    chmod +x /usr/local/bin/ghcup && \
    ghcup config set gpg-setting GPGStrict

# install GHC and Cabal
RUN ghcup install ghc --isolate /usr/local --force 8.10.7
RUN ghcup install cabal --isolate /usr/local/bin --force 3.6.2.0
RUN cabal update

# Install some Futhark dependencies
RUN apt-get install -y libgmp-dev libtinfo-dev

# Finally install Futhark via Cabal
RUN cabal install --install-method=copy --installdir=/usr/local/bin futhark
