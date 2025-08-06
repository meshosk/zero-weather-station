sudo apt update
sudo apt upgrade -y

sudo install mc pip -y

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install spidev numpy Pillow

git clone https://github.com/GregDMeyer/IT8951
cd IT8951
pip install ./[rpi]
cd ..
