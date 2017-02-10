# py-ads1256
Python Library with wrapers to read 8 channels from the Texas Instruments ADS1256 ADC.

## Installation

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


## Testing

Please run this to test:

    python test.py


## Learn by example

To understand, let's analyze this simple example:

    import ads1256
    ads1256.inicia(str(1),"2d5") 
    ValorDosCanais = ads1256.leia_canais()
    print ValorDosCanais[0]
    print ValorDosCanais[1]
    print ValorDosCanais[2]
    print ValorDosCanais[3]
    print ValorDosCanais[4]
    print ValorDosCanais[5]
    print ValorDosCanais[6]
    print ValorDosCanais[7]
    ads1256.termina()


The "ads1256.inicia()" function take two arguments: the ADC gain and the ADC SPS.


ADC Gain is one of the following

    1,  2,  4,  8,  16,  32,  64



SPS (Samples per Second) is one of the following

    2d5,  5,  10,  15,  25,  30,  50,  60,  100,  500,  1000,  2000,  3750,  7500,  15000,  30000



After this, funcion "ads1256.leia_canais()" reads the absolute values from ADC to an array with 8 positions.


Finally, the values are show on the console.  The "ads1256.termina()"  end the use of the ADC.


