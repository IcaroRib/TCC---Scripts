from sklearn.cluster import KMeans
import numpy as np
import MySQLdb
from time import time
from sklearn import metrics
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score

import itertools
from scipy import linalg
from sklearn import mixture
import matplotlib.pyplot as plt
import matplotlib as mpl

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
    "WHERE FL.documento IN (SELECT documento  "
    "			FROM fornecedores_licitacao "
    "            GROUP BY documento "
    "            HAVING count(licitacao_id) >= '" + str(min_licitacoes) + "') "
    "ORDER BY documento")

    cursor = db.cursor()

    data_set = []
    fornecedores = {}
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


def plot_results(X, Y_, means, covariances, index, title):

    color_iter = itertools.cycle(['navy', 'c', 'cornflowerblue', 'gold',
                              'darkorange'])
    
    splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-9., 5.)
    plt.ylim(-3., 6.)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)


sample_size = 300
data_set = np.array(montarDataSet(3,2))
for k in range (1,2):

    inicio = time()    
    mistura = mixture.GaussianMixture(n_components=k, covariance_type='full').fit(data_set)
    plot_results(data_set, mistura.predict(data_set), mistura.means_, mistura.covariances_, 0,'Gaussian Mixture')

    fim = time()
    print 'Tempo Gasto: %f' %(fim - inicio)
