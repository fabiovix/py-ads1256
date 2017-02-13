import ads1256
import time,random

# Recebe o horario atual desde read_channelo epoch (Unix Time). 
# Usamos como uma "ancora", como ponto de inicio para medir o tempo desde esse ponto na execucao do programa.
d0 =time.time()

# Inicializa o ADC usando funcao da biblioteca py-ads1256
# Primeiro argumento: Ganho. O segundo eh o SPS
# Ganho pode ser:  1,  2,  4,  8,  16,  32,  64
# SPS pode ser:    2d5,  5,  10,  15,  25,  30,  50,  60,  100,  500,  1000,  2000,  3750,  7500,  15000,  30000
ads1256.start("1","2d5")
 

# Calcula e exibe quanto tempo se passou desde o inicio do programa ate o fim da execucao da funcao de inicializacao
print str(int((time.time()-d0)*1000))+"mS in initializing ADC\n"


# Realiza 5 leituras de todos os canais do ADC. 
print "\nReading all channels with the function ads1256.read_all_channels():"
for i in range(1):
    d0 =time.time()
    valorTodosCanais = ads1256.read_all_channels()
    for x in valorTodosCanais:
        print x
    print "\n" + str(int((time.time()-d0)*1000))+"mS elapsed in reading 8 channels (" + str(int((time.time()-d0)*1000)/8) + " mS in each one)\n" 

 

#Realiza a leitura do canal 0 do ADC
print "\nReading only the channel 0 with ads1256.read_channel():"
d0 =time.time()
valorCanal = ads1256.read_channel(1)
print valorCanal
        
print "\n" + str(int((time.time()-d0)*1000))+"mS in reading only channel 0\n"
 

print ads1256.stop()
print "\n[OK] --- done with success."
