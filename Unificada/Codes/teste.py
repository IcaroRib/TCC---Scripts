from sklearn.cluster import KMeans
import numpy as np
import MySQLdb
import matplotlib.pyplot as plt
import time
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score
from sklearn.metrics import pairwise_distances
from sklearn import preprocessing

import urllib
import json

def save(cluster,cnpj): 
    url = "https://www.receitaws.com.br/v1/cnpj/" + str(cnpj)
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    arq = open("Jsons/"+str(cluster)+"__"+str(cnpj)+".json","w")
    json.dump(data,arq)
    arq.close()

def update(cnpjs):
    db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )
    
    alteracoes = []
    for cluster,array in cnpjs.iteritems():
        if len(array) < 100:
           alteracoes += array

    string = str(alteracoes)
    string = string.replace("[","")
    string = string.replace("]","")
    sql = "UPDATE fornecedores SET clusterizado = '1' WHERE cnpj IN (%s)" %(string)

    print sql

    cursor = db.cursor()
    cursor.execute(sql)
    

def cnpjs(min_licitacoes):
    db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )
    
    sql_fornecedores = ("SELECT FL.documento, FL.licitacao_id "
    "FROM fornecedores_licitacao FL "
    "INNER JOIN licitacoes L ON (L.id = FL.licitacao_id AND (modalidade = 2 or modalidade =3 or modalidade = 11) ) "
    "WHERE FL.documento not like '000%' AND FL.documento IN (SELECT documento  "
    "			FROM fornecedores_licitacao "
    "            GROUP BY documento "
    "            HAVING count(licitacao_id) >= '" + str(min_licitacoes) + "') "
    "ORDER BY documento")

    cursor = db.cursor()
    
    cnpjs = []

    cursor.execute(sql_fornecedores)
    for i in cursor:
        fornecedor = i[0]
        if fornecedor not in cnpjs:
            cnpjs.append(fornecedor)

    return cnpjs

def montarDataSet(min_fornecedores,min_licitacoes):
    db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )

    sql_licitacoes = ("SELECT L.id "
    "FROM licitacoes L "
    "WHERE (modalidade = 2 or modalidade = 3 or modalidade = 11) "
    "AND L.id IN (SELECT licitacao_id "
    "			FROM fornecedores_licitacao "
    "            GROUP BY licitacao_id "
    "            HAVING count(id) >= '" + str(min_fornecedores) + "') "
    "ORDER BY 1 ")

    sql_fornecedores = ("SELECT FL.documento, FL.licitacao_id "
    "FROM fornecedores_licitacao FL "
    "INNER JOIN licitacoes L ON (L.id = FL.licitacao_id AND (modalidade = 2 or modalidade =3 or modalidade = 11) ) "
    "WHERE FL.documento not like '000%' AND FL.documento IN (SELECT documento  "
    "			FROM fornecedores_licitacao "
    "            GROUP BY documento "
    "            HAVING count(licitacao_id) >= '" + str(min_licitacoes) + "') "
    "ORDER BY documento")

    cursor = db.cursor()

    data_set = []
    fornecedores = {}
    cnpjs = []
    licitacoes = []

    cursor.execute(sql_licitacoes)
    cont = 0
    for i in cursor:
        licitacoes.append(i[0])

    cursor.execute(sql_fornecedores)
    for i in cursor:
        fornecedor = i[0]
        participacao = i[1]
        if fornecedor in fornecedores:
            fornecedores[fornecedor].append(participacao)
        else:
            fornecedores[fornecedor] = [participacao]
            cnpjs.append(fornecedor)
                    
    for fornecedor in fornecedores:

        participacoes = fornecedores[fornecedor]
        array = []
        for licitacao in licitacoes:
        
            if licitacao in participacoes:
                array.append(1)
            else:
                array.append(0)
                
        data_set.append(array)


    return data_set


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))


sample_size = 300
data_set = np.array(montarDataSet(1,2))
docs = cnpjs(2)
cnpjs = {}

pca = PCA(n_components=2)
pca.fit(data_set)
pca_data = pca.transform(data_set)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

for k in range (8,9):
    
    estimator = KMeans(n_clusters=k, random_state=3).fit(pca_data)

    centroids = estimator.cluster_centers_
    labels = estimator.labels_
    silhueta = metrics.silhouette_score(data_set, labels, metric='hamming')
    silhueta_2 = metrics.silhouette_score(data_set, labels, metric='euclidean')

    print 'K = %i | SSE = %i ' %(k,estimator.inertia_)

    len_clusters = [0] * k

    for i in range(len(pca_data)):

        color = colors[labels[i]]
        plt.scatter(pca_data[i][0],pca_data[i][1],s=5,c='b')
        
        len_clusters[labels[i]] +=1
        
        if labels[i] not in cnpjs:
            cnpjs[labels[i]] = []
            
        cnpjs[labels[i]].append(docs[i])            

    for i in range(k):
        print "Cluster %i Size %i" %(i,len_clusters[i])

plt.show()
#update(cnpjs)

##for cluster,array in cnpjs.iteritems():
##    if cluster != 5 and len(array) > 1:
##        print 'Cluster ' + str(cluster) + ' - CNPJS: ',
##        print array
##        for cnpj in array:
##            try:
##                save(cluster,cnpj)
##            except:
##                print cnpj
##            time.sleep(5)
