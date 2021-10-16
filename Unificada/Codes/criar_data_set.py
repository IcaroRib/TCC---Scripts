import MySQLdb

db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )

min_fornecedores = 3
min_licitacoes = 2

data_set = open("fornecedores_dataset_61.arff","w")
data_set.write("@relation fornecedores_dataset_61 \n \n")

sql_licitacoes = ("SELECT L.id, L.vencedor "
"FROM licitacoes L "
"WHERE (modalidade = 2 or modalidade = 3 or modalidade = 11) AND vencedor is not null "
"AND vencedor IN (SELECT cnpj FROM fornecedores WHERE clusterizado = 1) "
"ORDER BY 1 ")

sql_fornecedores = ("SELECT FL.documento, FL.licitacao_id "
"FROM fornecedores_licitacao FL "
"INNER JOIN licitacoes L ON (L.id = FL.licitacao_id AND (modalidade = 2 or modalidade =3 or modalidade = 11) ) "
"INNER JOIN fornecedores F ON (F.cnpj = FL.documento AND clusterizado = 1 ) "
"ORDER BY documento")

cursor = db.cursor()

fornecedores = {}
licitacoes = []
first = True
string_vencedor = " { '"

hel = []

cursor.execute(sql_fornecedores)
cont = 0
for i in cursor:
    documento = str(i[0])
    licitacao = i[1]   

    if documento not in fornecedores:
        fornecedores[documento] = []
        data_set.write("@attribute '" + documento + "' { n, y } \n")

        if first == True:
            first = False
            string_vencedor += documento + "' "
        else:
            string_vencedor += ", '" + documento + "'"
    
    fornecedores[documento].append(licitacao)

string_vencedor += " }"
data_set.write("@attribute vencedor" + string_vencedor + "\n")
data_set.write("\n\n@data \n")
cursor.execute(sql_licitacoes)
for i in cursor:

    linha = ""
    licitacao = i[0]
    vencedor = str(i[1])
    
    for fornecedor in fornecedores:
        
        participacoes = fornecedores[fornecedor]    
        if licitacao in participacoes:
            linha += "y,"
        else:
            linha += "n,"

    linha += "'"+vencedor+"'"
    linha += "\n"
    linha = linha.replace(",\n","\n")
    data_set.write(linha)

    if vencedor not in hel:
        hel.append(vencedor)

data_set.close()
cursor.close()
db.close()
