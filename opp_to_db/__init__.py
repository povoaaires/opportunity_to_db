import logging
import pyodbc
import json
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
        row = ConectSql('dml',query)
        if row == None:
            query = f"INSERT INTO Clientes ([Nome],[Sobrenome],[Email],[Telefone],[DataNascimento],[Endereco],\
                [Cidade],[Estado],[CEP],[Pais],[DataCadastro],[CPF])\
                    VALUES ({req['NomePessoa']},{req['NomePessoa'].split(" ")[1]},{req['Email']}, \
                        {req['Telefone']},{req['DataNascimento']},{req['Endereco']},{req['Cidade']},\
                            {req['Estado']},{req['CEP']},{str(datetime.now())},{req['NomePessoa']},{req['Cpf']})"
            
            row = ConectSql('ddl',query)
            print(row)
            
    except:
        pass





def ConectSql(tipo,query):
    try:
        cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=NTB-64VKH93\SQLEXPRESS;DATABASE=crm_auto_fast;Trusted_Connection=yes;")
        cursor = cnxn.cursor()  
        if tipo == 'ddl':
            count = cursor.execute(query).rowcount
            cnxn.commit()
            fim = str(count)
            return fim
        elif tipo == 'dml':
            cursor.execute(query) 
            row = cursor.fetchone() 
            return str(row)
    except Exception as ex:
        return ex