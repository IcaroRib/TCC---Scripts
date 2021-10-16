import statistics

for i in range(5,11):
    file = "results_apriori_" + str(i)
    arq = open(file,"r")
    linhas = arq.readlines()
    arq.close()
    confiancas = []

    for linha in linhas:
        array = linha.split('<conf:(')

        conf = ""
        for c in array[1]:        
            if c ==')':
                break
            conf = conf + c
        confiancas.append(float(conf))

    tamanho = len(confiancas)
    media = statistics.mean(confiancas) 
    variancia = statistics.variance(confiancas) 
    print ("%i\%% & %i & %0.4f & %0.4f \\\\ " % (i,tamanho,media,variancia)  )
