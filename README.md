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


## Learn by example 1: reading a single channel

    import ads1256                                   # import this lib
    ads1256.start(str(1),"25")                       # initialize the ADC using 25 SPS with GAIN of 1x
    ChannelValue = ads1256.read_channel(0)           # read the value from ADC channel 0 
    print ChannelValue                               # print the value from the variable
    ads1256.stop()                                   # stop the use of the ADC


## Learn by example 2: reading all the channels at once

    import ads1256                                   # import this lib
    ads1256.start(str(1),"25")                       # initialize the ADC using 25 SPS with GAIN of 1x
    AllChannelValues = ads1256.read_all_channels()   # create a list of 8 elements: one for each ADC channel 
    for x in AllChannelValues:                       # for loop... 
        print x                                      # ...print each of the list elements
    ads1256.stop()                                   # stop the use of the ADC
 
 
## The arguments

The "ads1256.start()" function take two arguments: the ADC gain and the ADC SPS.


ADC Gain is one of the following

    1,  2,  4,  8,  16,  32,  64



SPS (Samples per Second) is one of the following

    2d5,  5,  10,  15,  25,  30,  50,  60,  100,  500,  1000,  2000,  3750,  7500,  15000,  30000

The 2d5 SPS equals to 2.5 (it's a nomenclature issue from the original C code)



After this, funcion "ads1256.leia_canais()" reads the absolute values from ADC to an array with 8 positions.
Finally, the values are show on the console.  The "ads1256.termina()"  end the use of the ADC.


