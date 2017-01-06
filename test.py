import ads1256


valoresDoCanal = ads1256.leia_canais("1","25")
for valorCanal in valoresDoCanal:
    print valorCanal

print "\n[OK] --- lib ads1256 compilada com sucesso!"
