import ads1256       # import this lib                             

gain = 1			 # ADC's Gain parameter
sps = 25			 # ADC's SPS parameter

AllChannelValuesVolts = [0,0,0,0,0,0,0,0]       # Create the first list. It will receive ADC's absolute values
AllChannelValues = [0,0,0,0,0,0,0,0]			# Create the second list. It will received absolute values converted to Volts

ads1256.start(str(gain),str(sps))                    # Initialize the ADC using the parameters
AllChannelValues = ads1256.read_all_channels()       # Fill the first list with all the ADC's absolute channel values 
                
for i in range(0, 8):             															
	AllChannelValuesVolts[i] = (((AllChannelValues[i] * 100) /167.0)/int(gain))/1000000.0   # Fill the second list  with the voltage values


for i in range(0, 8):                      
    print AllChannelValues[i]              # Print all the absolute values


print ("\n");							   # Print a new line


for i in range(0, 8):                      
    print AllChannelValuesVolts[i]         # Print all the Volts values converted from the absolute values


ads1256.stop() 							   # Stop the use of the ADC



     