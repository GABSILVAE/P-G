#!/bin/bash

sudo apt update
sudo apt install git
git clone https://github.com/jeremyb31/rtl8192eu-linux-driver
cd rtl8192eu-linux-driver
export ARCH=arm64
make
sudo make install
echo "blacklist rtl8xxxu" | sudo tee /etc/modprobe.d/rtl8xxxu.conf;
echo -e "8192eu\n\nloop" | sudo tee /etc/modules;
sudo update-grub; sudo update-initramfs -u;
systemctl reboot -i;