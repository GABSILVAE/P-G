#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#gedit ~/.bashrc
#export PATH=${PATH}:/usr/local/cuda/bin
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64
#~/.bashrc

sudo apt-get install cmake
sudo apt-get install python3-pip
sudo -H pip3 install wget
sudo -H pip3 install Cython
sudo apt-get install libboost-all-dev
sudo apt-get install python3-numpy
sudo apt-get install python3-pillow
sudo apt-get install build-essential python3-dev python3-setuptools libboost-python-dev libboost-thread-dev
nvcc --version
pip3 install pycuda




