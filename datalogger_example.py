import ads1256                  # import the ads1256 lib                             
import time                     # import the time lib
from datetime import datetime   # import the datetime lib

#Python example to use the ADS1256 as a Voltage Data Logger.  

gain = 1			 # ADC's Gain parameter. Possible values:  1,  2,  4,  8,  16,  32,  64
sps = "25"			 # ADC's SPS parameter. Possible values:   2d5,  5,  10,  15,  25,  30,  50,  60,  100,  500,  1000,  2000,  3750,  7500,  15000,  30000

chv = [0,0,0,0,0,0,0,0]       # Create the first list. It will receive ADC's absolute values
ch     = [0,0,0,0,0,0,0,0]			# Create the second list. It will received absolute values converted to Volts

ads1256.start(str(gain),str(sps))                    # Initialize the ADC using the parameters
 

# Define the CSV filename based on the date and time
timest = str(datetime.now())
timest = timest.replace(":", "_")
timest = timest.replace(" ", "-")
timest = timest.replace(".", "-")
timest = timest[:-7]
filename = "ads1256-log-"+str(timest)+".csv"


header =[]            
header.extend(["Row_id","Channel 0","Channel 1","Channel 2","Channel 3","Channel 4","Channel 5","Channel 6","Channel 7","Timestamp"])   # Define a CSV header 


with open(filename,"w") as file:        						# With the opened file...
   file.write(",".join(str(value) for value in header)+ "\n")   # Write each value from the header 


i = 0 
ch= [0,0,0,0,0,0,0,0]

print ("ADS1256 Voltage Data Logger" + "\n" + "GAIN: " + str(gain) + "    SPS: " + str(sps)  + "   FILENAME:  " + filename + "\n")


with open(filename,"a") as file:           # Open the file into Append mode (enter data without erase previous data)

    while True:     # Forever loop
    		
            
            
                
                row_id = i

                ch = ads1256.read_all_channels()       # Fill the first list with all the ADC's absolute channel values 
                
                for x in range(0, 8):
                    chv[x] = (((ch[x] * 100) /167.0)/int(gain))/1000000.0   # Fill the second list  with the voltage values

                print str(chv[0]) + " " + str(chv[1]) + " " + str(chv[2]) + " " + str(chv[3]) + " " + str(chv[4]) + " " + str(chv[5]) + " " + str(chv[6])+ " " + str(chv[7])

                # Registra efetivamente no arquivo .CSV  (no padrao americano)
                file.write(str(row_id) 
                + ", " + str(chv[0]) + ", " + str(chv[1]) + ", " + str(chv[2]) 
                + ", " + str(chv[3]) + ", " + str(chv[4]) + ", " + str(chv[5]) 
                + ", " + str(chv[6]) + ", " + str(chv[7]) + ", " + str(datetime.now()) + "\r\n")

                time.sleep(0.1)   # That's the time the program will wait until the next read. To use higher SPS, use a lower sleep value, of miliseconds
                i = i + 1


# Stop the use of the ADC
ads1256.stop() 							   



     
