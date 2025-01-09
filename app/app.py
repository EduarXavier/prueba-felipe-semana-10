import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from redis import Redis
from elasticsearch import Elasticsearch

app = Flask(__name__)

with open(os.getenv('MONGO_USER_FILE'), 'r') as file:
    mongo_user = file.read().strip()

with open(os.getenv('MONGO_PASSWORD_FILE'), 'r') as file:
    mongo_password = file.read().strip()

with open(os.getenv('MONGO_DB_NAME_FILE'), 'r') as file:
    mongo_db_name = file.read().strip()

# Configuraciones de conexión usando variables de entorno
mongo_client = MongoClient(
    host=os.getenv('MONGO_HOST', 'mongodb.docker'),
    port=int(os.getenv('MONGO_PORT', 27017)),
    username=mongo_user,
    password=mongo_password
)
mongo_db = mongo_client[mongo_db_name]
redis_client = Redis(host=os.getenv('REDIS_HOST', 'redis.docker'), port=int(os.getenv('REDIS_PORT', 6379)), decode_responses=True)
es_client = Elasticsearch([{
    'host': os.getenv('ES_HOST', 'elasticsearch'),
    'port': int(os.getenv('ES_PORT', 9200)),
    'scheme': 'http'
}])

# Endpoint para MongoDB
@app.route('/mongo', methods=['POST'])
def insert_mongo():
    data = request.json
    mongo_db['data'].insert_one(data)
    return jsonify({"message": "Dato insertado en MongoDB"})

@app.route('/mongo', methods=['GET'])
def get_mongo():
    data = list(mongo_db['data'].find({}, {'_id': 0}))
    return jsonify(data)

# Endpoint para Redis
@app.route('/redis', methods=['POST'])
def insert_redis():
    data = request.json
    for key, value in data.items():
        redis_client.set(key, value)
    return jsonify({"message": "Datos insertados en Redis"})

@app.route('/redis/<key>', methods=['GET'])
def get_redis(key):
    value = redis_client.get(key)
    if value:
        return jsonify({key: value})
    return jsonify({"error": "Clave no encontrada"})

# Endpoint para Elasticsearch
@app.route('/elasticsearch', methods=['POST'])
def insert_elasticsearch():
    data = request.json
    es_client.index(index=os.getenv('ES_INDEX', 'data_index'), body=data)
    return jsonify({"message": "Dato insertado en Elasticsearch"})

@app.route('/elasticsearch', methods=['GET'])
def get_elasticsearch():
    results = es_client.search(index=os.getenv('ES_INDEX', 'data_index'), body={"query": {"match_all": {}}})
    return jsonify(results['hits']['hits'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)))

