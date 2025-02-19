from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Altere para seu usuário MySQL
    'password': 'menu1234',  # Altere para sua senha MySQL
    'database': 'entregadores_db'  # Nome do seu banco de dados
}

# Função para obter a conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def menu():
    return render_template('menu.html')

@app.route('/cadastro', methods=['GET'])
def cadastro_form():
    return render_template('cadastrar_entregador.html')

@app.route("/cadastro", methods=['POST'])
def cadastro():
    try:
        dados = request.form
        campos_obrigatorios = [
            'nome', 'telefone', 'email', 'endereco', 'modalidade', 'unidade',
            'cpf', 'nome_fila', 'chave_pix', 'data_nascimento', 'canal_vaga'
        ]
        
        # Validação dos campos obrigatórios
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo].strip():
                return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO entregadores (nome, telefone, email, endereco, modalidade, unidade, cpf, cnpj, nome_fila, chave_pix, data_nascimento, canal_vaga)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dados["nome"], dados["telefone"], dados["email"], dados["endereco"],
            dados["modalidade"], dados["unidade"], dados["cpf"], dados.get("cnpj", ""),
            dados["nome_fila"], dados["chave_pix"], dados["data_nascimento"], dados["canal_vaga"]
        ))

        conn.commit()
        return jsonify({"mensagem": "Entregador cadastrado com sucesso!"}), 201
    
    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro ao inserir no banco de dados: {err}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/consulta")
def ficha():
    return render_template('consulta_entregador.html')

@app.route('/api/busca_ficha', methods=['GET'])
def buscar_ficha():
    codigo = request.args.get('codigo')

    if not codigo:
        return jsonify({"erro": "Código do entregador não fornecido"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT nome, unidade, modalidade, relacao FROM entregadores WHERE codigo = %s"
        cursor.execute(query, (codigo,))
        entregador = cursor.fetchone()

        if entregador:
            return jsonify(entregador)
        else:
            return jsonify({"erro": "Entregador não encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro ao conectar ao banco de dados: {err}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Rodar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
