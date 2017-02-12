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
for i in range(1):
    d0 =time.time()
    valoresDosCanais = ads1256.read_all_channels()
    for x in valoresDosCanais:
        print x
    print str(int((time.time()-d0)*1000))+"mS used in reading 8 channels (" + str(int((time.time()-d0)*1000)/8) + " mS in each one)\n" 

 

d0 =time.time()
valorDoCanal = ads1256.read_channel("wancharle")
print "canais: \n" 
for x in valorDoCanal:
        print x
print str(int((time.time()-d0)*1000))+"mS in reading this last channel\n"

 


print ads1256.stop()
print "\n[OK] --- done with success."
