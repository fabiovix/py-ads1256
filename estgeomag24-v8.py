# Nesta versao (v08), as novidades sao:
# - Inclusao da leitura de dois sensores de temperatura MCP9808
# - Inclusao de compensacao de drift de temperatura
# Autor:  Fabio Franco de Oliveira
# Email:  fabioti6@gmail.com
# Ultima alteracao: 05/01/2016


# Importa algumas bibliotecas de sistema
import time
import os
import sys
import decimal
import math
from datetime import datetime
import Adafruit_MCP9808.MCP9808 as MCP9808

# Configura o nome base para o arquivo csv
BASENAME = "EstGeoMag24-v8"

#Inicia a contagem de linhas
row_id = 1

# Seta o ganho do ADC
GANHO = 1

# Instancia e inicializa o sensor MCP9808
#sensor1 = MCP9808.MCP9808(address=0x18)
#sensor2 = MCP9808.MCP9808(address=0x19)
#sensor1.begin()
#sensor2.begin()

# Funcao criada a partir dos exemplos da AdaFruit para fazer a leitura do ADC
def ReadEstGeoMag():

    # Variaveis: a, b, c, d sao para os valores absolutos do ADC
    #            t, u, v, w sao para os valores em Volts convertidos a partir dos absolutos
    #            x, y, z    sao para os valores em nT convertidos a partir das voltagens
    a=0; b=0; c=0; d=0; t=0; u=0; v=0; w=0; x=0; y=0; z=0; ModACE=0; ModPRT=0; ModXYZ=0; ModXYZ_fix=0; p_fix=0; r_fix=0; t_fix=0; x_fix=0; y_fix=0; z_fix=0; DeltaH=0; DeltaH_fix=0;
       

    #Leitura dos sensores de temperatura
    headtemp = 20
    bodytemp = 20 
    #headtemp = sensor1.readTempC()  
    #bodytemp = sensor2.readTempC()  

    # Calcula a variacao da temperatura em relacao ao valor otimo (para 20 graus)
    #temp_diff = headtemp - 20

       
    # Cria um lista de tres posicoes
    ValorDoCanal = [0]*8

    resposta_comando = os.popen("./ads1256_test 0 " + str(GANHO) + " 2d5")

    # Inicia a leitura dos valores absolutos dos tres canais do ADC para as variaveis a b c
    ValorDoCanal[0] = (long(resposta_comando.readline())) 
    ValorDoCanal[1] = (long(resposta_comando.readline())) 
    ValorDoCanal[2] = (long(resposta_comando.readline())) 
    ValorDoCanal[3] = (long(resposta_comando.readline())) 
    ValorDoCanal[4] = (long(resposta_comando.readline())) 
    ValorDoCanal[5] = (long(resposta_comando.readline())) 
    ValorDoCanal[6] = (long(resposta_comando.readline())) 
    ValorDoCanal[7] = (long(resposta_comando.readline())) 
    
    a = ValorDoCanal[0]     
    b = ValorDoCanal[1]  
    c = ValorDoCanal[2] 
    d = ValorDoCanal[3]
    e = ValorDoCanal[4]
    f = ValorDoCanal[5]
    g = ValorDoCanal[6]
    h = ValorDoCanal[7]

    # Calcula os valores em Volts de acordo com o ganho configurado para as variaveis x y z
       
    p = (((a * 100) /167.0)/GANHO)/1000000.0 
    q = (((b * 100) /167.0)/GANHO)/1000000.0
    r = (((c * 100) /167.0)/GANHO)/1000000.0  
    s = (((d * 100) /167.0)/GANHO)/1000000.0 
    t = (((e * 100) /167.0)/GANHO)/1000000.0
    u = (((f * 100) /167.0)/GANHO)/1000000.0
    v = (((g * 100) /167.0)/GANHO)/1000000.0  
    w = (((h * 100) /167.0)/GANHO)/1000000.0

    #p = (((a * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #q = (((b * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #r = (((c * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #s = (((d * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #t = (((e * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #u = (((f * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #v = (((g * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    #w = (((h * 100) /167.77216)/GANHO)/1000000.0   valor considerando 2^24 bits
    


    # Subtrai a referencia OUT -  (V e W nao inclusos por medirem a fonte)
    p = p - q
    r = r - s 
    t = t - u

    

    # Calcula valor em teslas
    x = ((p * 50.0/1.0) * 1000.0)
    y = ((r * 50.0/1.0) * 1000.0)
    z = ((t * 50.0/1.0) * 1000.0)
    
 
        

    #Calcula o modulo dos canais
    ModACE = math.sqrt (a**2 + c**2 + e**2)    
    ModPRT = math.sqrt (p**2 + r**2 + t**2)
    ModXYZ = math.sqrt (x**2 + y**2 + z**2)


    #Calcula DeltaH   
    DeltaH = math.sqrt (x**2 + y**2)
    

    #Em caso de variacao de temp, calcula a saida alternativa ModXYZ_FIX com calculo de drift
    #if (temp_diff != '0'):

  
        #Corrige os valores de ref dos FLC que sao alimentados pelo LP2981 usando fator calculado conforme mensurado por mim
        #O ideal nessa formula seria reduzir o modulo e nao assumir os sinais positivo e negativo nas subtracoes
        #p_fix =  p - (temp_diff * 0.000213889)
        #r_fix =  r + (temp_diff * 0.000186111)
        #t_fix =  t + (temp_diff * 0.000187500)

 
        # Calcula valor em teslas com compensacao usando fator menor que 2nT por grau conforme datasheet do FLC-100
        #O ideal nessa formula seria reduzir o modulo e nao assumir os sinais positivo e negativo nas subtracoes
        #x_fix = ((p_fix * 50.0/1.0) * 1000.0) - (temp_diff * 1.5)
        #y_fix = ((r_fix * 50.0/1.0) * 1000.0) + (temp_diff * 1.5)
        #z_fix = ((t_fix * 50.0/1.0) * 1000.0) + (temp_diff * 1.5)

         
        #Calcula o modulo dos canais
        #ModXYZ_fix = math.sqrt (x_fix**2 + y_fix**2 + z_fix**2)

        #Calcula DeltaH com drift
        #DeltaH_fix = math.sqrt (x_fix**2 + y_fix**2) 



    #Retorna todos os valores das variaveis
    return a, b, c, d, e, f, g, h, ModACE, p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ, ModXYZ_fix, headtemp, bodytemp, DeltaH, DeltaH_fix



 

# Aqui comeca a rotina principal do EstGeoMag 
# Recurso que criei para retornar data e hora que nao contenham caracteres ilegais para sistemas Windows
datetime_fix = str(datetime.now())
datetime_fix = datetime_fix.replace(":", "_")
datetime_fix = datetime_fix.replace(" ", "-")
datetime_fix = datetime_fix.replace(".", "-")

# Define como sera o nome do arquivo exportado .CSV
filename = BASENAME+"-"+str(datetime_fix)+".csv"

# Monta os cabecalhos do arquivo .CSV - "a b c" sao valores absolutos e "t y c" sao os convertidos em volts
header =[]
header.extend(["Row_id","Mag_a","Mag_b","Mag_c","Mag_d","Mag_e","Mag_f","Mag_g","Mag_h","Mod_abe","Mag_p","Mag_q","Mag_r","Mag_s","Mag_t","Mag_u","Mag_v", "Mag_w","Mod_PRT", "Mag_x", "Mag_y", "Mag_z", "Mag_xyz", "Mag_xyz_fix","Headtemp","Bodytemp","Deltah","DeltaH_fix" , "Timestamp"]) 

# Escreve em disco os cabecalhos no arquivo
with open(filename,"w") as file:
  # Usando virgula como separador de colunas
  file.write(",".join(str(value) for value in header)+ "\n")

  # Usando ponto-e-virgula como separador de colunas
  #file.write(";".join(str(value) for value in header)+ "\n")


# Comeca a preparar a leitura dos valores de acordo com os argumentos passados em linha de comando
if len(sys.argv) >= 3 and sys.argv[1].find("-n") == 0:
    n = decimal.Decimal(sys.argv[2])
    dlay = 0
    if len(sys.argv) >= 4:
        dlay = decimal.Decimal(sys.argv[3])
  
    print("")
    print("EstGeoMag24 v8 - Capturando %d amostras com intervalo de %d mS" % (n, dlay))
    print("")
    fdlay = 0.0
    fdlay = dlay / 1000    
   #fdlay = (dlay / 1000) - 497 
    i = 0
    samples = []
          
    print("q          s          u          v          w            MagX       MagY     MagZ       ModXYZ   ModXYZ_Fix  HTemp    BTemp  DeltaH    DeltaH_Fix")
    while n > 0:
       
        # Faz a leitura dos 3 canais
        (a, b, c, d, e, f, g, h, ModACE, p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ, ModXYZ_fix, headtemp, bodytemp, DeltaH, DeltaH_fix) = ReadEstGeoMag()
        

        # Exibe em tempo real na tela
        print("%8.8f %8.8f %8.8f %8.8f %8.8f   %8.2f  %8.2f  %8.2f  %8.2f %8.3f %8.3f %8.3f %8.3f %8.3f" % (q, s, u, v, w, x, y, z, ModXYZ, ModXYZ_fix, headtemp, bodytemp, DeltaH, DeltaH_fix))

        # Abre o arquivo em modo Append (incluir dados sem sobrescrever)
        with open(filename,"a") as file:
                  
            # Registra efetivamente no arquivo .CSV  (no padrao americano)
            file.write(str(row_id) + ", " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ", " + str(e) + ", " + str(f) + ", " 
            + str(g) + ", " + str(h) + ", " + str(format(ModACE, '8.8f')) + ", " + str(format(p, '8.8f')) + ", " + str(format(q, '8.8f')) 
            + ", " + str(format(r, '8.8f')) + ", " + str(format(s, '8.8f')) + ", " + str(format(t, '8.8f')) + ", " + str(format(u, '8.8f')) 
            + ", " + str(format(v, '8.8f')) + ", " + str(format(w, '8.8f')) + ", " + str(format(ModPRT, '8.8f')) + ", " + str(format(x, '8.8f')) 
            + ", " + str(format(y, '8.8f')) + ", " + str(format(z, '8.8f')) + ", " + str(format(ModXYZ, '8.8f')) + ", " + str(format(ModXYZ_fix, '8.8f'))
            + ", " + str(format(headtemp, '8.4f')) + ", " + str(format(bodytemp, '8.4f')) + ", " + str(format(DeltaH, '8.8f')) + ", " + str(format(DeltaH_fix, '8.8f')) 
            + ", " + str(datetime.now()) + "\r\n")
                       
        # Atualiza a contagem de linhas 
        row_id = row_id + 1
    
        # Acrescenta as leituras na lista
        samples = samples + [[a, b, c, d, e, f, g, h, ModACE, p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ]]
        i = i + 1
        n = n - 1
        time.sleep(fdlay)


    # Demais rotinas para calculo das medias e desvio padrao    
    MP = MQ = MR = MS = MT = MU = MV = MW = X = Y = Z = MP2 = MQ2 = MR2 = MS2 = MT2 = MU2 = MV2 = MW2 = MedP = MedQ = MedR = MedS = MedT = MedU = MedV = 0.0
    MedW = DesvPadP = DesvPadQ = DesvPadR = DesvPadS = DesvPadT = DesvPadU = DesvPadV = DesvPadW = ModMedPRT = ModMedXYZ = DesvPadModPRT = DesvPadModXYZ = 0.0
    MA = MB = MC = MD = ME = MF = MG = MH = MX = MY = MZ = MX2 = MY2 = MZ2 = MA2 = MB2 = MC2 = MD2 = ME2 = MF2 = MG2 = MH2 = MedA = MedB = MedC = 0.0
    MedD = MedW = MedX = MedY = MedZ = DesvPadA = DesvPadB = DesvPadC = DesvPadX = DesvPadY = DesvPadZ = DesvPadD = ModMedACE = ModMedXYZ = DesvPadModACE = headtemp = bodytemp = DeltaH = DeltaH_fix= 0.0 

    for (a, b, c, d, e, f, g, h, ModACE, p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ, ModXYZ_fix) in samples:
        
        MA = MA + a
        MB = MB + b
        MC = MC + c
        MD = MD + d
        ME = ME + e
        MF = MF + f
        MG = MG + g
        MH = MH + h
        MP = MP + p
        MQ = MQ + q
        MR = MR + r
        MS = MS + s
        MT = MT + t
        MU = MU + u
        MV = MV + v        
        MW = MW + w
        MX = MX + x
        MY = MY + y
        MZ = MZ + z
        

    MedA = MA / i
    MedB = MB / i
    MedC = MC / i
    MedD = MD / i
    MedE = ME / i
    MedF = MF / i
    MedG = MG / i
    MedH = MH / i
    MedP = MP / i
    MedQ = MQ / i
    MedR = MR / i
    MedS = MS / i
    MedT = MT / i
    MedU = MU / i
    MedV = MV / i
    MedW = MW / i
    MedX = MX / i
    MedY = MY / i
    MedZ = MZ / i
    

    for (a, b, c, d, e, f, g, h, ModACE, p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ) in samples:
        
        MA2 = MA2 + (a - MedA) ** 2
        MB2 = MB2 + (b - MedB) ** 2
        MC2 = MC2 + (c - MedC) ** 2
        MD2 = MD2 + (d - MedD) ** 2
        ME2 = ME2 + (e - MedE) ** 2
        MF2 = MF2 + (f - MedF) ** 2
        MG2 = MG2 + (g - MedG) ** 2
        MH2 = MH2 + (h - MedH) ** 2
        MP2 = MP2 + (p - MedP) ** 2
        MQ2 = MQ2 + (q - MedQ) ** 2
        MR2 = MR2 + (r - MedR) ** 2
        MS2 = MS2 + (s - MedS) ** 2
        MT2 = MT2 + (t - MedT) ** 2
        MU2 = MU2 + (u - MedU) ** 2
        MV2 = MV2 + (v - MedV) ** 2        
        MW2 = MW2 + (w - MedW) ** 2     
        MX2 = MX2 + (x - MedX) ** 2
        MY2 = MY2 + (y - MedY) ** 2
        MZ2 = MZ2 + (z - MedZ) ** 2
        
    
    DesvPadA = math.sqrt(MA2 / (i-1))
    DesvPadB = math.sqrt(MB2 / (i-1))
    DesvPadC = math.sqrt(MC2 / (i-1))
    DesvPadD = math.sqrt(MD2 / (i-1))
    DesvPadE = math.sqrt(ME2 / (i-1))
    DesvPadF = math.sqrt(MF2 / (i-1))
    DesvPadG = math.sqrt(MG2 / (i-1))
    DesvPadH = math.sqrt(MH2 / (i-1))
    DesvPadP = math.sqrt(MP2 / (i-1))
    DesvPadQ = math.sqrt(MQ2 / (i-1))
    DesvPadR = math.sqrt(MR2 / (i-1))
    DesvPadS = math.sqrt(MS2 / (i-1))
    DesvPadT = math.sqrt(MT2 / (i-1))
    DesvPadU = math.sqrt(MU2 / (i-1))
    DesvPadV = math.sqrt(MV2 / (i-1))
    DesvPadW = math.sqrt(MW2 / (i-1))
    DesvPadX = math.sqrt(MX2 / (i-1))
    DesvPadY = math.sqrt(MY2 / (i-1))
    DesvPadZ = math.sqrt(MZ2 / (i-1))
    

    ModMedACE = math.sqrt(MedA**2 + MedC**2 + MedE**2)   
    ModMedPRT = math.sqrt(MedP**2 + MedR**2 + MedT**2)    
    ModMedXYZ = math.sqrt(MedX**2 + MedY**2 + MedZ**2)
   
    DesvPadModACE = math.sqrt((DesvPadA**2) + (DesvPadC**2) + (DesvPadE**2))
    DesvPadModPRT = math.sqrt((DesvPadP**2) + (DesvPadR**2) + (DesvPadT**2))
    DesvPadModXYZ = math.sqrt((DesvPadX**2) + (DesvPadY**2) + (DesvPadZ**2))
	 
    print("")
    print("     Media                 Desvio Padrao")
    print("mP   %8.8f            %8.8f" % (MedP, DesvPadP))
    print("mQ   %8.8f            %8.8f" % (MedQ, DesvPadQ))
    print("mR   %8.8f            %8.8f" % (MedR, DesvPadR))
    print("mS   %8.8f            %8.8f" % (MedS, DesvPadS))

    print("")
    print("mT   %8.8f            %8.8f" % (MedT, DesvPadT))
    print("mU   %8.8f            %8.8f" % (MedU, DesvPadU))
    
    print("mV   %8.8f            %8.8f" % (MedV, DesvPadV))
    print("mW   %8.8f            %8.8f" % (MedW, DesvPadW))
    print("")
    print("mX   %8.8f        %8.8f" % (MedX, DesvPadX))
    print("mY   %8.8f        %8.8f" % (MedY, DesvPadY))
    print("mZ   %8.8f       %8.8f" % (MedZ, DesvPadZ))
    print("")
  
    print("")
    print("     Modulo Medias         Modulo Desvio Padrao")
    print("mACE %8.12f        %8.12f" % (ModMedACE, DesvPadModACE))
    print("mPRT %8.12f        %8.12f" % (ModMedPRT, DesvPadModPRT))
    print("mXYZ %8.12f   %8.12f" % (ModMedXYZ, DesvPadModXYZ))
    print("")


    # Abre o arquivo em modo Append (incluir dados sem sobrescrever)
    with open(filename,"a") as file:

     # Registra efetivamente no arquivo .CSV  (no padrao americano)
     file.write("\n" + ", " + "Media mA:" + ", " + str(format(MedA, '.8f')) + ", " + "Desvio Padrao mA:" + ", " + str(format(DesvPadA, '.8f')) + " \r\n")
     file.write       (", " + "Media mB:" + ", " + str(format(MedB, '.8f')) + ", " + "Desvio Padrao mB:" + ", " + str(format(DesvPadB, '.8f')) + " \r\n")
     file.write       (", " + "Media mC:" + ", " + str(format(MedC, '.8f')) + ", " + "Desvio Padrao mC:" + ", " + str(format(DesvPadC, '.8f')) + " \r\n")
     file.write       (", " + "Media mD:" + ", " + str(format(MedD, '.8f')) + ", " + "Desvio Padrao mD:" + ", " + str(format(DesvPadD, '.8f')) + " \r\n")
     file.write       (", " + "Media mE:" + ", " + str(format(MedE, '.8f')) + ", " + "Desvio Padrao mE:" + ", " + str(format(DesvPadE, '.8f')) + " \r\n")
     file.write       (", " + "Media mF:" + ", " + str(format(MedF, '.8f')) + ", " + "Desvio Padrao mF:" + ", " + str(format(DesvPadF, '.8f')) + " \r\n")
     file.write       (", " + "Media mG:" + ", " + str(format(MedG, '.8f')) + ", " + "Desvio Padrao mG:" + ", " + str(format(DesvPadG, '.8f')) + " \r\n")
     file.write       (", " + "Media mH:" + ", " + str(format(MedH, '.8f')) + ", " + "Desvio Padrao mH:" + ", " + str(format(DesvPadH, '.8f')) + " \r\n")
     file.write       (", " + "Media mP:" + ", " + str(format(MedP, '.8f')) + ", " + "Desvio Padrao mP:" + ", " + str(format(DesvPadP, '.8f')) + " \r\n")
     file.write       (", " + "Media mQ:" + ", " + str(format(MedQ, '.8f')) + ", " + "Desvio Padrao mQ:" + ", " + str(format(DesvPadQ, '.8f')) + " \r\n")
     file.write       (", " + "Media mR:" + ", " + str(format(MedR, '.8f')) + ", " + "Desvio Padrao mR:" + ", " + str(format(DesvPadR, '.8f')) + " \r\n")
     file.write       (", " + "Media mS:" + ", " + str(format(MedS, '.8f')) + ", " + "Desvio Padrao mS:" + ", " + str(format(DesvPadS, '.8f')) + " \r\n")
     file.write       (", " + "Media mT:" + ", " + str(format(MedT, '.8f')) + ", " + "Desvio Padrao mT:" + ", " + str(format(DesvPadT, '.8f')) + " \r\n")
     file.write       (", " + "Media mU:" + ", " + str(format(MedU, '.8f')) + ", " + "Desvio Padrao mU:" + ", " + str(format(DesvPadU, '.8f')) + " \r\n")
     file.write       (", " + "Media mV:" + ", " + str(format(MedV, '.8f')) + ", " + "Desvio Padrao mV:" + ", " + str(format(DesvPadV, '.8f')) + " \r\n")
     file.write       (", " + "Media mW:" + ", " + str(format(MedW, '.8f')) + ", " + "Desvio Padrao mW:" + ", " + str(format(DesvPadW, '.8f')) + " \r\n")
     file.write       (", " + "Media mX:" + ", " + str(format(MedX, '.8f')) + ", " + "Desvio Padrao mX:" + ", " + str(format(DesvPadX, '.8f')) + " \r\n")
     file.write       (", " + "Media mY:" + ", " + str(format(MedY, '.8f')) + ", " + "Desvio Padrao mY:" + ", " + str(format(DesvPadY, '.8f')) + " \r\n")
     file.write       (", " + "Media mZ:" + ", " + str(format(MedZ, '.8f')) + ", " + "Desvio Padrao mZ:" + ", " + str(format(DesvPadZ, '.8f')) + " \r\n")
     file.write       (", " + "Modulo Medias mACE:" + ", " + str(format(ModMedACE, '.8f')) + ", " + "Desvio Padrao Modulo mABE:" + ", " + str(format(DesvPadModACE, '.12f')) + " \r\n")
     file.write       (", " + "Modulo Medias mPRT:" + ", " + str(format(ModMedPRT, '.12f')) + ", " + "Desvio Padrao Modulo mPRT:" + ", " + str(format(DesvPadModPRT, '.12f')) + " \r\n")
     file.write       (", " + "Modulo Medias mXYZ:" + ", " + str(format(ModMedXYZ, '.12f')) + ", " + "Desvio Padrao Modulo mXYZ:" + ", " + str(format(DesvPadModXYZ, '.12f')) + " \r\n")
     file.write("\n" + ", " + "EstGeoMag24 V8" +"\r\n")


	 # Registra o ganho setado no programa 
     file.write       (", " + "Ganho setado em: " + str(GANHO) +"\r\n")  

	 # Registra a quantidade de amostras capturadas alem do intervalo configurado
     file.write       (", " + "Foram capturadas " + str(decimal.Decimal(sys.argv[2])) + " amostras com intervalo de " + str(decimal.Decimal(sys.argv[3])) + " mS" + " entre elas" + "\r\n")
         
 
# No caso de execucao do programa sem se passar argumentos   
# Realiza a leitura somente uma vez, exibindo na tela e armazenando em arquivo
else:
    
    # Faz a leitura dos 3 canais
    (p, q, r, s, t, u, v, w, ModPRT, x, y, z, ModXYZ) = ReadEstGeoMag()
    print 'p = %8.8f, q = %8.8f, r = %8.8f, s = %8.8f, t = %8.8f, u = %8.8f, v = %8.8f, w = %8.8f, ModPRT = %8.8f, magX = %8.8f, magY = %8.8f, magZ = %8.8f' % (p, q, r, s, t, u, v, w, x, y, z)
    
    # Abre o arquivo em modo Append (incluir dados sem sobrescrever)
    with open(filename,"a") as f:
      # Registra efetivamente no arquivo .CSV  (no padrao americano)
      file.write(str(row_id) + ", " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(format(t, '.8f')) + str(format(u, '.8f')) + str(format(v, '.8f')) + str(format(d, '.8f')) + str(format(w, '.8f')) + str(format(x, '.8f')) + ", " + str(format(y, '.8f')) + ", " + str(format(z, '.8f')) + ", " + str(datetime.now()) + "\r\n")

       
