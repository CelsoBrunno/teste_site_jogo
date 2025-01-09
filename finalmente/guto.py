from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file, abort, flash
import os
import io
import re
from werkzeug.utils import secure_filename
from db_connection import get_db_connection
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Configuração do diretório de upload temporário
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
 
# Rota Home
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

# Rota Cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        try:
            nome_empresa = request.form["nome"]
            area_empresa = request.form["area"]
            email_empresa = request.form["email"]
            linguagens = request.form["linguagem"]
            ferramentas = request.form["frameworks"]
            desafio_empresa = request.form["desafio"]
            arquivo = request.files.get("arquivo")

            if not nome_empresa or not area_empresa or not email_empresa or not linguagens:
                return jsonify({"success": False, "error": "Por favor, preencha todos os campos obrigatórios e envie um arquivo."})

            arquivo_binario = arquivo.read()
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """INSERT INTO empresas (nome_empresa, area_empresa, email_empresa, linguagens, ferramentas, desafio_empresa, arquivo_pdf, status_empresa) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, 'em analise')"""
            cursor.execute(query, (nome_empresa, area_empresa, email_empresa, linguagens, ferramentas, desafio_empresa, arquivo_binario,))
            conn.commit()
            return jsonify({"success": True, "message": "Cadastro realizado e arquivo salvo no banco!"})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    return render_template("cadastro.html")

# Função para validar formato de e-mail
def validar_email(email):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email)

# @app.route("/verificar_email", methods=["POST"])
# def verificar_email():
#     try:
#         email = request.json.get("email")
#         if not validar_email(email):
#             return jsonify({"success": False, "error": "E-mail inválido. Insira um e-mail válido."})

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "SELECT * FROM empresas WHERE email_empresa = %s"
#         cursor.execute(query, (email,))
#         resultado = cursor.fetchone()
#         cursor.close()

#         if resultado:
#             return jsonify({"success": True, "status": resultado[0], "message": "Acesso liberado com sucesso!"})
#         else:
#             return jsonify({"success": False, "error": "E-mail não encontrado no sistema."})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

@app.route("/verificar_email", methods=["POST"])
def verificar_email():
    try:
        email = request.json.get("email")
        if not validar_email(email):
            return jsonify({"success": False, "error": "E-mail inválido. Insira um e-mail válido."})

        conn = get_db_connection()

        with conn.cursor() as cursor:
            query = "SELECT * FROM empresas WHERE email_empresa = %s"
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()
            
            # Consuma todos os resultados restantes, caso existam
            cursor.fetchall()

        if resultado:
            return jsonify({"success": True, "status": resultado[0], "message": "Acesso liberado com sucesso!"})
        else:
            return jsonify({"success": False, "error": "E-mail não encontrado no sistema."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    finally:
        if conn.is_connected():
            conn.close()



# Rota Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        if not validar_email(email):
            return render_template("login.html", error="E-mail inválido.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empresas WHERE email_empresa = %s", (email,))
        resultado = cursor.fetchone()

        if resultado:
            session["usuario_logado"] = email
            return redirect(url_for("status_emp"))
        else:
            return render_template("login.html", error="E-mail não encontrado no sistema.")
    
    return render_template("login.html")

@app.route("/status_emp")
def status_emp():
    if "usuario_logado" not in session:
        return redirect(url_for("login"))

    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT nome_empresa, desafio_empresa, status_empresa FROM empresas WHERE email_empresa = %s"
            cursor.execute(query, (session["usuario_logado"],))
            status_result = cursor.fetchone()

            # Consuma todos os resultados restantes
            cursor.fetchall()

        if status_result:
            return render_template("empresa_status.html", **status_result)
        else:
            return "Nenhuma informação encontrada para a empresa."

    except Exception as e:
        return f"Erro ao buscar dados: {str(e)}"

    finally:
        if conn.is_connected():
            conn.close()

# Rota Status
# @app.route("/status_emp")
# def status_emp():
#     if "usuario_logado" not in session:
#         return redirect(url_for("login"))

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = "SELECT nome_empresa, desafio_empresa, status_empresa FROM empresas WHERE email_empresa = %s"
#         cursor.execute(query, (session["usuario_logado"],))
#         status_result = cursor.fetchone()

#         if status_result:
#             return render_template("empresa_status.html", **status_result)
#         else:
#             return "Nenhuma informação encontrada para a empresa."

#     except Exception as e:
#         return f"Erro ao buscar dados: {str(e)}"

#     finally:
#         cursor.close()
#         conn.close()

# Rota Adm
@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        login = request.form["email"]
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nome_empresa FROM empresas WHERE id_empresa = 102")
        login_admin = cursor.fetchone()

        if login_admin and login == login_admin["nome_empresa"]:
            session["admin"] = True
            return redirect(url_for("status_admin"))

        error_message = "Credenciais inválidas."
        return render_template("login_admin.html", error=error_message)

    return render_template("login_admin.html")

@app.route("/status_admin", methods=["GET", "POST"])
def status_admin():
    if "admin" not in session:
        return redirect(url_for("login_admin"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consulta todas as informações necessárias
        cursor.execute("SELECT id_empresa, nome_empresa, desafio_empresa, status_empresa FROM empresas")
        desafios = cursor.fetchall()

        # Atualiza a session para manter os IDs das empresas
        session["id_empresa"] = []
        desafios_formatados = []

        for desafio in desafios:
            # Atualizando a session com os IDs
            session["id_empresa"].append(desafio["id_empresa"])
            
            # Adiciona o desafio no formato necessário
            desafios_formatados.append({
                "id_empresa": desafio["id_empresa"],
                "nome_empresa": desafio["nome_empresa"],
                "desafio_empresa": desafio["desafio_empresa"],
                "status_empresa": desafio["status_empresa"]
            })

        return render_template("status_admin.html", desafios=desafios_formatados)

    except Exception as e:
        return f"Erro ao buscar dados: {str(e)}"

    finally:
        cursor.close()
        conn.close()

@app.route("/download/<int:id>")
def download(id):
    if "id_empresa" not in session or id not in session["id_empresa"]:
        abort(403, "Acesso negado.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT arquivo_pdf, nome_empresa FROM empresas WHERE id_empresa = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            arquivo_binario, nome_empresa = result
            nome_arquivo = f"{nome_empresa}_{id}.pdf"
            pdf_file = io.BytesIO(arquivo_binario)
            pdf_file.seek(0)

            return send_file(
                pdf_file,
                as_attachment=True,
                download_name=nome_arquivo,
                mimetype="application/pdf"
            )
        else:
            abort(404, "Arquivo não encontrado.")

    except Exception as e:
        abort(500, f"Erro ao buscar arquivo: {str(e)}")

    finally:
        conn.close()

@app.route("/aprovar/<int:empresa_id>", methods=["POST"])
def aprovar(empresa_id):
    if "id_empresa" not in session or empresa_id not in session["id_empresa"]:
        abort(403, "Acesso negado.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE empresas SET status_empresa = 'Aprovado' WHERE id_empresa = %s"
        cursor.execute(query, (empresa_id,))
        conn.commit()
        return redirect(url_for("status_admin"))

    except Exception as e:
        return f"Erro ao aprovar: {str(e)}"

    finally:
        conn.close()

@app.route("/recusar/<int:empresa_id>", methods=["POST"])
def recusar(empresa_id):
    if "id_empresa" not in session or empresa_id not in session["id_empresa"]:
        abort(403, "Acesso negado.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE empresas SET status_empresa = 'Recusado' WHERE id_empresa = %s"
        cursor.execute(query, (empresa_id,))
        conn.commit()
        return redirect(url_for("status_admin"))

    except Exception as e:
        return f"Erro ao recusar: {str(e)}"

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
