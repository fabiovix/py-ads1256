# py-ads1256
Python Library with wrapers to read 8 channels from the Texas Instruments ADS1256 ADC.  
It does make use of the original WaveShare's C library for the [High-Precision_AD/DA_Board 24 Bits] (http://www.waveshare.com/wiki/High-Precision_AD/DA_Board) 

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

Please run one of these to test

    python read_example.py
    python read_volts_example.py
    python datalogger_example.py 
 


## Learn by example 1: reading a single channel's absolute value

    import ads1256                                   # import this lib
    ads1256.start(str(1),"25")                       # initialize the ADC using 25 SPS with GAIN of 1x
    ChannelValue = ads1256.read_channel(0)           # read the value from ADC channel 0 
    print ChannelValue                               # print the value from the variable
    ads1256.stop()                                   # stop the use of the ADC



## Learn by example 2: reading the absolute values from all the channels at once

    import ads1256                                   # import this lib
    ads1256.start(str(1),"25")                       # initialize the ADC using 25 SPS with GAIN of 1x
    AllChannelValues = ads1256.read_all_channels()   # create a list of 8 elements: one for each ADC channel 
    for x in AllChannelValues:                       # for each element in the list... 
        print x                                      # ...print it
    ads1256.stop()                                   # stop the use of the ADC
 



## Learn by example 3: reading all the channels in absolute values and in voltage values

    import ads1256       # import this lib                             

    gain = 1             # ADC's Gain parameter
    sps = 25             # ADC's SPS parameter

    AllChannelValuesVolts = [0,0,0,0,0,0,0,0]       # Create the first list. It will receive ADC's absolute values
    AllChannelValues = [0,0,0,0,0,0,0,0]            # Create the second list. It will received absolute values converted to Volts

    ads1256.start(str(gain),str(sps))                    # Initialize the ADC using the parameters
    AllChannelValues = ads1256.read_all_channels()       # Fill the first list with all the ADC's absolute channel values 
                    
    for i in range(0, 8):                                                                       
        AllChannelValuesVolts[i] = (((AllChannelValues[i] * 100) /167.0)/int(gain))/1000000.0   # Fill the second list  with the voltage values

    for i in range(0, 8):                      
        print AllChannelValues[i]              # Print all the absolute values

    print ("\n");                              # Print a new line

    for i in range(0, 8):                      
        print AllChannelValuesVolts[i]         # Print all the Volts values converted from the absolute values

    ads1256.stop()                             # Stop the use of the ADC




## Explaining the arguments

The "ads1256.start()" function take two arguments: the ADC gain and the ADC SPS.


ADC Gain is one of the following

    1,  2,  4,  8,  16,  32,  64



SPS (Samples per Second) is one of the following

    2d5,  5,  10,  15,  25,  30,  50,  60,  100,  500,  1000,  2000,  3750,  7500,  15000,  30000

The 2d5 SPS equals to 2.5 (it's a nomenclature issue from the original C code. It should by passed this way in the Python)




## A Voltage Data Logger

    I've included a example to use the ads1256 as a Voltage Data Logger. 
    It keeps reading all the ads1256 channels in absolute and voltage values and saving to a CSV file until a break from the user
    To test it, run the following:

    python datalogger_example.py



 

