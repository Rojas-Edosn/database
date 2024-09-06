from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to help with conversion
import os

app = Flask(__name__)

# Obtenha a URI a partir da variável de ambiente ou defina diretamente aqui para teste local
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb+srv://AssuntoCrisp:<db_password>@assuntoscrisp.sxetv.mongodb.net/?retryWrites=true&w=majority&appName=AssuntosCrisp")

# Conecta ao cluster MongoDB Atlas
client = MongoClient(MONGO_URI)

# Selecione o banco de dados
db = client["Assuntos"]

# Selecione a coleção
collection = db["Crisp.Assuntos Crisp"]

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Recebe os dados JSON do webhook
        data = request.json
        
        # Insere os dados na coleção do MongoDB
        result = collection.insert_one(data)
        
        # Adiciona o _id ao retorno e converte para string
        data["_id"] = str(result.inserted_id)
        
        # Retorna uma resposta de sucesso
        return jsonify({"status": "sucesso", "data": data}), 200
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    # Obtém a porta a partir da variável de ambiente PORT ou usa 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    # Executa o servidor na porta obtida
    app.run(host='0.0.0.0', port=port)
