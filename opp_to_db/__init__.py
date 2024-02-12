import logging
import pyodbc
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req = req.json()
        logging.info("Registro lido com Sucesso em seu devido formado")

    except Exception:
        logging.error("Erro ao ler o body, dicionário fora do padrão estabelecido")
        return func.HttpResponse(
             "Erro ao ler o body, dicionário fora do padrão estabelecido",
             status_code=500
        )
    
    connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=NTB-64VKH93;DATABASE=crm_auto_fast;UID=usersystem;PWD=8fdKJl3$nlNv3049jsKK")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM dbo.Clientes")
    row = cursor.fetchone()
    print(row)

