import logging
import pyodbc
import json
import os
import fstrings
import azure.functions as func
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req = req.get_json()
        logging.info("Registro lido com Sucesso em seu devido formado")

    except Exception as ex:
        logging.error(f"Erro ao ler o body, dicionário fora do padrão estabelecido -> {ex}")
        return func.HttpResponse(
             "Erro ao ler o body, dicionário fora do padrão estabelecido",
             status_code=500
        )
    
    try:
        query = f"SELECT CPF from Clientes where CPF = '{req['Cpf']}';"
        cursor = ConectSql()
        cursor.execute(query) 
        row = cursor.fetchone()

        if str(row) == 'None':
            date_today = datetime.today()
            insert = "INSERT INTO Clientes ([Nome],[Sobrenome],[Email],[Telefone],[DataNascimento],[Endereco],[Cidade],[Estado],[CEP],[Pais],[CPF]) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
            cursor = ConectSql()
            count = cursor.execute(insert,req['NomePessoa'],req['NomePessoa'],req['Email'],req['Telefone'],req['DataNasc'],req['Endereco'],req['Cidade'],req['Estado'],req['CEP'],req['Pais'],req['Cpf']).rowcount
            count.commit()
            fim = str(count)
            variavel_teste = 2
            if fim >= 1:
                logging.info("Cliente criado com Sucesso na base")
            else:
                logging.info("Falha ao criar o cliente na base")
                

                        
            
            # row = ConectSql('ddl',query)
            # print(row)
            
    except Exception as ex:
        print(ex)





def ConectSql():
    try:
        cnxn = pyodbc.connect(os.environ["connectionDB"])
        cursor = cnxn.cursor()  
        return cursor
    except Exception as ex:
        return ex