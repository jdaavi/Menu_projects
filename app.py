from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',  # Altere para seu usuário MySQL
    'password': 'menu1234',  # Altere para sua senha MySQL
    'database': 'entregadores_db'  # Nome do seu banco de dados
}

@app.route("/")
def menu():
  return render_template('menu.html')

@app.route("/cadastro")
def cadastro():
  return render_template('cadastrar_entregador.html')


@app.route("/consulta")
def ficha():
    return render_template('consulta_entregador.html')

@app.route('/api/busca_ficha', methods=['GET'])
def buscar_ficha():
    codigo = request.args.get('codigo')  # Pega o código pela URL (ex: ?codigo=12345)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    if not codigo:
        return jsonify({"erro": "Código do entregador não fornecido"}), 400
    
    # Conectar ao banco de dados
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Verifique se o nome da coluna está correto, no caso foi alterado para 'relacao' (sem acento)
        query = "SELECT nome, unidade, modalidade, relacao FROM entregadores WHERE codigo = %s"
        cursor.execute(query, (codigo,))
        
        # Obter o resultado
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
