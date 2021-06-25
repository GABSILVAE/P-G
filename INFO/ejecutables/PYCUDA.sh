#!/bin/bash
# -*- ENCODING: UTF-8 -*-

sudo apt-get install cmake
sudo apt-get install python3-pip
sudo -H pip3 install wget
sudo -H pip3 install Cython
sudo apt-get install libboost-all-dev
sudo apt-get install python3-numpy
sudo apt-get install python3-pillow
sudo apt-get install build-essential python3-dev python3-setuptools libboost-python-dev libboost-thread-dev
echo "export PATH=${PATH}:/usr/local/cuda/bin"
echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64"
sudo gedit ~/.bashrc
source ~/.bashrc
nvcc --version
pip3 install pycuda
python3
import pycuda
exit()



