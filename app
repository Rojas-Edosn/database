from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to help with conversion
import os

app = Flask(__name__)

# Utilizando uma variável de ambiente para a string de conexão do MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["Assuntos"]
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
    # Executa o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000)
