arq = open('/home/icaro/TCC/Paraíba/contador_vitorias.txt','r')
vitorias = arq.readlines()
cont1 = 0
cont2 = 0
cont3 = 0
cont4 = 0
cont5 = 0

for v in vitorias:
    tupla = v.split(';')
    cnpj = tupla[0]
    num = int(tupla[1].replace('\n',''))
    if num > 1 and num <=2:
        cont1 +=1
    if num > 2 and num <= 4:
        cont2 +=1
    if num > 4 and num <= 12:
        cont3 +=1
    if num >12:
        cont4 +=1
    if num >30:
        cont5 +=1

print(cont1)
print(cont2)
print(cont3)
print(cont4)
print(cont5)
