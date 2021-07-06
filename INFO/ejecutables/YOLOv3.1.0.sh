#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

sudo apt update
git clone https://github.com/puigalex/deteccion-objetos-video.git
cd deteccion-objetos-video
sudo apt-get install libopencv-dev
sudo apt-get install python3-opencv
sudo apt-get install build-essential
sudo apt-get install cmake
sudo apt-get install pkg-config
sudo apt-get install libgtk2.0-dev python3-dev python3-numpy
sudo apt-get install libjpeg-dev libtiff5-dev libopenexr-dev libtbb-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev
bash weights/download_weights.sh
mv yolov3.weights weights/

#sudo -H pip3 install torch
sudo apt-get install python3-pip libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install future
sudo -H pip3 install --upgrade setuptools
sudo -H pip3 install Cython
sudo -H pip3 install gdown
sudo cp ~/.local/bin/gdown /usr/local/bin/gdown
gdown https://drive.google.com/uc?id=12UiREE6-o3BthhpjQxCKLtRg3u4ssPqb
sudo -H pip3 install torch-1.9.0a0+gitd69c22d-cp36-cp36m-linux_aarch64.whl
rm torch-1.9.0a0+gitd69c22d-cp36-cp36m-linux_aarch64.whl

sudo -H pip3 install torchvision
sudo -H pip3 install tqdm

sudo reboot

#https://qengineering.eu/install-pytorch-on-jetson-nano.html
#torch.cuda.is_available()
#python3 deteccion_video.py
