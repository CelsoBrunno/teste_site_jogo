import mysql.connector
from mysql.connector import Error

db_config = {
    'user': 'root',  # Substitua pelo username do RDS
    'password': 'Banco2024',  # Substitua pela senha definida no RDS
    'host': 'bancodb.ct628qm8yfig.us-east-2.rds.amazonaws.com',  # Endpoint do banco RDS
    'port': '3306',  # Porta padrão do MySQL
    'database': 'bdprojeto',  # Substitua pelo nome do banco criado no RDS
}

def get_db_connection():
    # Usando 'with' para garantir o fechamento da conexão automaticamente
    conn = mysql.connector.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database']
    )
    return conn

        
    #     if connection.is_connected():
    #         print("Conexão bem sucedida ")
    #         return connection
    # except Error as e:
    #     print(f"Erro ao conectar ao banco de dados: {e} ")
    #     return None

# def close_connection(connection):
#     if connection.is_connected():
#         connection.close()
#         print("Conexão finalizada com o banco de dados")