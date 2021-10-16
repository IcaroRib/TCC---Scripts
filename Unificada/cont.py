arq = open('contador_vitorias.txt','r')
arq2 = open('results_apriori_10','r')
arq3 = open('results_apriori_censored.csv','w')
cv = arq.readlines()
apriori = arq2.readlines()
fornecedores = []

arq.close()
arq2.close()

for v in cv:
    tupla = v.split(';')
    cnpj = tupla[0]
    fornecedores.append(cnpj)

for a in apriori:
    a = a.split(')> lift:')[0]
    a = a.replace('<conf:(','')
    for f in fornecedores:
        if f in a:
            censurado = f[:2] + "*" + f[12:]
            a = a.replace(f,censurado)
    a = a[4:]
    a = a.replace(" ",";")
    a = a.replace(";;",";")
    a = a.replace(";;",";")
    arq3.write(a+"\n")
    

arq3.close()
