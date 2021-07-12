#!/bin/bash
# -*- ENCODING: UTF-8 -*-

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential cmake pkg-config
sudo apt-get -y install libgtk2.0-dev
sudo apt-get -y install libusb-1.0-0-dev
sudo apt-get -y install git git-core
sudo apt-get -y install python3 python3-scipy python3-matplotlib cython python3-dev python3-numpy 
sudo apt-get -y install python3-opencv
sudo apt-get -y install libglut3-dev 
sudo apt-get -y install freeglut3-dev 
sudo apt-get -y install libxmu-dev 
sudo apt-get -y install libxi-dev 
sudo apt-get -y install freenect
git clone https://github.com/OpenKinect/libfreenect.git
cd libfreenect
cd wrappers
cd python
sudo python3 setup.py install
#freenect-cppview
