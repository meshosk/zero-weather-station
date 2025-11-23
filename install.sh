#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

sudo apt install pip -y

python -m venv .venv

source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install spidev numpy pillow scipy openmeteo_requests retry_requests requests_cache pandas
pip install cairosvg ijson

# this should be pulled as submodule For cas it was not uncomment line below
# git clone https://github.com/GregDMeyer/IT8951
cd external/IT8951
pip install ./[rpi]
cd ../..

# pip install pytest-playwrightpip3 install scipy
# playwright install-deps
# playwright install chromiums

# now we run the namedays json fix script
python fix_namedays_json.py external/nameday-api/json/namedays.json assets/namedays_fixed.json
