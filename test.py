import ads1256
import time,random

# Recebe o horario atual desde o epoch (Unix Time). 
# Usamos como uma "ancora", como ponto de inicio para medir o tempo desde esse ponto na execucao do programa.
d0 =time.time()

# Inicializa o ADC usando funcao da biblioteca py-ads1256
ads1256.start("1","2d5")

# Calcula e exibe quanto tempo se passou desde o inicio do programa ate o fim da execucao da funcao de inicializacao
print str(int((time.time()-d0)*1000))+"ms na inicializacao"

# Realiza 5 leituras de todos os canais do ADC. 
for i in range(5):
    d0 =time.time()
    valoresDoCanal = ads1256.read_all_channels()
    for valorCanal in valoresDoCanal:
        print valorCanal
    print str(int((time.time()-d0)*1000))+"ms na leitura"
print ads1256.stop()
print "\n[OK] --- lib ads1256 compilada com sucesso !!!"
