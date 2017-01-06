import ads1256
import time,random

d0 =time.time()
ads1256.inicia("1","2d5")
print str(int((time.time()-d0)*1000))+"ms na inicializacao"
for i in range(5):
    d0 =time.time()
    valoresDoCanal = ads1256.leia_canais()
    for valorCanal in valoresDoCanal:
        print valorCanal
    print str(int((time.time()-d0)*1000))+"ms na leitura"
print ads1256.termina()
print "\n[OK] --- lib ads1256 compilada com sucesso!"
