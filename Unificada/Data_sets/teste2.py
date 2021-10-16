arq = open("fornecedores_dataset_apriori.arff","r")

lines = arq.readlines()
arq.close()
att = []
val = []

for i in range (0,len(lines)):
    if '@attribute' in lines[i]:
        att.append(lines[i])

found = False
for i in range (0,len(lines)):   
    if '@data' in lines[i]:
        found = True
    if found == True:
        val.append(lines[i])

dic = {}
final = []
for i in range (0,len(val)):    
    line = val[i]
    for j in range (0,len(line)):
        if line[j] == 'y':
            index = int(j/2)
            if index not in dic:                
                dic[index] = 0
            dic[index] = dic[index] + 1
            final.append(line)
            break

new = open("fornecedores_dataset_last.arff","w")
new.write('@relation fornecedores_dataset_61\n\n')

listdic = []
for k in dic:
    listdic.append(k)
    new.write(att[k])

classe = '@attribute vencedor { '
for f in final:
    l = f.split(',')
    sub = l[-1].replace("\n","")
    if sub not in classe:
        classe = classe + sub
classe = classe + ' }'

new.write(classe)
new.write('\n@data\n')
listdic.sort()
for f in final:
    listData = f.split(",")
    linha = ""    
    for k in listdic:
        linha = linha + listData[k] + ','
        
    linha = linha + listData[-1]
    new.write(linha)
    
new.close()
