import os
from db_connection import get_db_connection

def get_desktop_path():
    """Retorna o caminho da área de trabalho do usuário."""
    if os.name == "nt":  # Windows
        return os.path.join(os.environ["USERPROFILE"], "Desktop")
    else:  # Unix/Linux/Mac
        return os.path.join(os.environ["HOME"], "Desktop")

def fetch_and_save_pdf(id, desktop_path):
    """Busca o arquivo BLOB no banco e salva como PDF na área de trabalho."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para buscar o arquivo pelo ID
        query = "SELECT arquivo_pdf, nome_empresa FROM empresas WHERE id_empresa = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            arquivo_binario, nome_empresa = result
            nome_arquivo = f"{nome_empresa}_{id}.pdf"
            caminho_arquivo = os.path.join(desktop_path, nome_arquivo)

            # Salvar o arquivo como PDF
            with open(caminho_arquivo, "wb") as file:
                file.write(arquivo_binario)

            print(f"Arquivo salvo com sucesso na área de trabalho: {caminho_arquivo}")
        else:
            print(f"Nenhum arquivo encontrado para o ID {id}.")
    except Exception as e:
        print(f"Erro ao buscar ou salvar o arquivo: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    desktop_path = get_desktop_path()  # Obter caminho da área de trabalho
    try:
        id_empresa = int(input("Digite o ID da empresa para baixar o arquivo PDF: "))
        fetch_and_save_pdf(id_empresa, desktop_path)
    except ValueError:
        print("Por favor, insira um número válido como ID.")
