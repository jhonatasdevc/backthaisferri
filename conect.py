import psycopg2
from psycopg2 import OperationalError

def get_conect():
    connection = None
    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',  # Esta é a porta mapeada do contêiner Docker
            database='ferri',
            user='postgres',
            password='1234'
        )
        print("Conexão bem-sucedida ao banco de dados PostgreSQL!")
        return connection
    except OperationalError as e:
        print(f"Erro: {e}")
        return None

