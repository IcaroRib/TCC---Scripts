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


listdic = []
print(att[0])
#for k in dic:
    #listdic.append(k)
    #print(att[k])
