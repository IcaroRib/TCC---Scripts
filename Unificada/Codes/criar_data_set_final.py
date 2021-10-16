import MySQLdb

db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )

min_fornecedores = 3
min_licitacoes = 2

data_set = open("fornecedores_dataset_final.arff","w")
data_set.write("@relation fornecedores_dataset_final \n \n")

sql_licitacoes = ("SELECT L.id, L.vencedor "
"FROM licitacoes L "
"WHERE (modalidade = 2 or modalidade = 3 or modalidade = 11) AND vencedor is not null "
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
"                       INNER JOIN licitacoes L ON (L.id = licitacao_id AND vencedor is not null AND (modalidade = 2 or modalidade =3 or modalidade = 11) ) "
"            GROUP BY documento "
"            HAVING count(licitacao_id) >= '" + str(min_licitacoes) + "') "
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
    
    fornecedores[documento].append(licitacao)

cursor.execute(sql_licitacoes)
for i in cursor:

    licitacao = i[0]
    vencedor = str(i[1])
    if vencedor not in hel:
        hel.append(vencedor)
        if first == True:
            first = False
            string_vencedor += vencedor + "' "
        else:
            string_vencedor += ", '" + vencedor + "'"   

        
string_vencedor += " }"
data_set.write("@attribute vencedor" + string_vencedor + "\n")


teste = []
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

    if vencedor not in teste:
        teste.append(vencedor)

data_set.close()
cursor.close()
db.close()
