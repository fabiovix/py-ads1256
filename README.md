# py-ads1256
Python Library with wrapers to read 8 channels from the Texas Instruments ADS1256 ADC.
Biblioteca Python com uso de wrappers para a leitura de 8 canais do ADS1256 da Texas Instruments.


Instalation

To install the library, first install it's principal dependency: the SoC bcm2835 library:
 
sudo apt-get install automake libtool
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.50.tar.gz
tar zxvf bcm2835-1.50.tar.gz
cd bcm2835-1.50
autoreconf -vfi
./configure
make
sudo make check
sudo make install


After this, run the following commands on a Raspberry Pi or other Debian-based OS system:

sudo apt-get install git build-essential python-dev
cd ~
git clone https://github.com/fabiovix/py-ads1256.git
cd py-ads1256
sudo python setup.py install

