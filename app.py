from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Obtenha a URI a partir da variável de ambiente
MONGO_URI = os.environ.get("MONGODB_URI")

# Conecta ao cluster MongoDB Atlas
client = MongoClient(MONGO_URI)

# Selecione o banco de dados e a coleção
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
    port = int(os.environ.get("PORT", 5000))  # Use a variável de ambiente PORT
    app.run(host='0.0.0.0', port=port)
