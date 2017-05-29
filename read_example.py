import ads1256
import time,random

# Receive the current time since the epoch (Unix Time). 
# It's used like a "anchor", like a point of start, to measure the time since 
# this point in the program execution
d0 =time.time()

# Initializes the ADC using py-ads1256 library function 
# First argument: GAIN. The second: SPS
# Possible settings:
# GAIN values:  1,  2,  4,  8,  16,  32,  64
# SPS values:   2d5,  5,  10,  15,  25,  30,  50,  60,  100,  
# SPS values:   500, 1000,  2000,  3750,  7500,  15000,  30000
ads1256.start("1","2d5")
 

# Calculates and displays how much time has elapsed from the start of the program 
# to the end of executing the initialization function
print str(int((time.time()-d0)*1000))+"mS in initializing ADC\n"


# Performs 5 readings of all ADC channels.
print "\nReading all channels with the function ads1256.read_all_channels():"
for i in range(1):
    d0 =time.time()
    valorTodosCanais = ads1256.read_all_channels()
    for x in valorTodosCanais:
        print x
    print "\n" + str(int((time.time()-d0)*1000))+"mS elapsed in reading 8 channels (" + str(int((time.time()-d0)*1000)/8) + " mS in each one)\n" 


# Performs the reading of ADC channel 0
print "\nReading only the channel 0 with ads1256.read_channel():"
d0 =time.time()
valorCanal = ads1256.read_channel(0)
print valorCanal
        
print "\n" + str(int((time.time()-d0)*1000))+"mS in reading only channel 0\n"
 

ads1256.stop()
