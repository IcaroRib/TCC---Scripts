import urllib
import json
import time
#!/usr/bin/python
import MySQLdb
import codecs

# Open database connection
db = MySQLdb.connect("localhost","root","Toushi9856","paraiba" )

cursor = db.cursor()

arq_ = open("cnpjs_falhos.txt","r")
falhos = arq_.readlines()
arq_.close()

arq__ =  open("cnpjs_falhos.txt","a")
arq = codecs.open('falhas.txt', 'a', encoding='utf8')

min_licitacoes = 2

sql_fornecedores = ("SELECT FL.documento, COUNT(FL.licitacao_id)"
    "FROM fornecedores_licitacao FL WHERE FL.documento not like '000%' "
    "AND FL.documento NOT IN (SELECT cnpj FROM paraiba.fornecedores) "
    "GROUP BY 1 HAVING count(licitacao_id) >= '" + str(min_licitacoes) + "' "
    "LIMIT 1000")

cursor.execute(sql_fornecedores)
cont = 0

time_start = time.time()
for i in cursor:
 
    cnpj = i[0]
    if cnpj in falhos:
        continue

    print "CNPJ " + cnpj ,
    
    if cont % 3 == 0:
        time_end = time.time()    
        
        if (time_end - time_start) < 30:
            time.sleep(30 - (time_end - time_start))

        time_start = time.time()
            
    
    url = "https://www.receitaws.com.br/v1/cnpj/" + cnpj
    cont +=1

    try:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print "- Download Concluido",

        capital_social = float(data['capital_social'])
        ultima_atualizacao = data['ultima_atualizacao']
        atividade_principal_text = data['atividade_principal'][0]['text']
        atividade_principal_code = data['atividade_principal'][0]['code']
        data_situacao = data['data_situacao']
        tipo = data['tipo']
        status = data['status']
        situacao = data['situacao']
        bairro = data['bairro'][:36]
        logradouro = data['logradouro'].replace("'","")
        numero = data['numero']
        cep = data['cep']
        municipio = data['municipio'].replace("'","")
        abertura = data['abertura']
        natureza_juridica = data['natureza_juridica']

        sql = ("INSERT INTO fornecedores (capital_social,ultima_atualizacao,cnpj,atividade_principal_text,atividade_principal_code,data_situacao, "
                "tipo, status,situacao,bairro,logradouro,numero,cep,municipio,abertura,natureza_juridica) "
                "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                "'%s','%s','%s','%s','%s')") %(capital_social,ultima_atualizacao,cnpj,atividade_principal_text,atividade_principal_code,data_situacao,
                  tipo, status,situacao,bairro,logradouro,numero,cep,municipio,abertura,natureza_juridica)

        try:            
            cursor.execute(sql)
            db.commit()
            print "- Insercao Concluida"

        except:
            string= "Insercao Falha: " + cnpj+"\n" + sql + "\n\n"
            arq.write(string)
            arq_.write(cnpj+"\n")
            db.rollback()
            print "- Insercao Falha"

        
    except:
        print "- Download Falho"
        
arq.close()
arq__.close()
