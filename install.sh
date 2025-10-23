#!/bin/bash

sudo apt update
sudo apt upgrade

sudo apt install mc pip -y

python -m venv .venv

source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install spidev numpy Pillow

# this should be pulled as submodule For cas it was not uncomment line below
# git clone https://github.com/GregDMeyer/IT8951

cd IT8951
pip install ./[rpi]
cd ..

pip install pytest-playwright
playwright install-deps
playwright install chromium

