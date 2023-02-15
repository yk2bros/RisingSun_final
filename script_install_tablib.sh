sudo apt install python3-pip
pip3 install virtualenv
virtualenv dummy
source dummy/bin/activate
python setup.py install
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
sudo apt-get install build-essential
sudo ./configure
sudo make
sudo make install
sudo apt upgrade
pip install ta-lib
echo "Installed TALIB"
