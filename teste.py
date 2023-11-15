import psycopg2
from psycopg2 import OperationalError

def get_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host='0.0.0.0',
            port='5433',  # Esta é a porta mapeada do contêiner Docker
            database='ferri',
            user='user_ferri',
            password='UmD&2987'
        )
        print("Conexão bem-sucedida ao banco de dados PostgreSQL!")
	
        return connection
    except OperationalError as e:
        print(f"Erro: {e}")
        return None



# Exemplo de uso:
connection = get_connection()
if connection is not None:
     # Executar operações no banco de dados aqui
     connection.close()  # Não se esqueça de fechar a conexão quando terminar
