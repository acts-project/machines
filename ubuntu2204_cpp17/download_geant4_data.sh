#!/bin/bash
set -e

data_dir=/usr/local/share/Geant4-10.6.1/data

mkdir $data_dir
cd $data_dir


function dl {
    url=$1
    echo "Downloading $url"
    curl --location $url | tar -xz
}

dl https://geant4-data.web.cern.ch/datasets/G4NDL.4.6.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4EMLOW.7.9.1.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4PhotonEvaporation.5.5.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4RadioactiveDecay.5.4.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4PARTICLEXS.2.1.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4PII.1.3.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4RealSurface.2.1.1.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4SAIDDATA.2.0.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4ABLA.3.1.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4INCL.1.0.tar.gz
dl https://geant4-data.web.cern.ch/datasets/G4ENSDFSTATE.2.2.tar.gz