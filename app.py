from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import os

app = Flask(__name__)
CORS(app)
db = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)

@app.route('/api/counter/increment', methods=['POST'])
def increment_counter():
    user_id = request.args.get('user_id')
    db.incr(user_id)
    return jsonify(success=True)

@app.route('/api/counter/decrement', methods=['POST'])
def decrement_counter():
    user_id = request.args.get('user_id')
    db.decr(user_id)
    return jsonify(success=True)

@app.route('/api/counter/reset', methods=['POST'])
def reset_counter():
    user_id = request.args.get('user_id')
    db.set(user_id, 0)
    return jsonify(success=True)

@app.route('/api/counter', methods=['GET'])
def get_counter():
    user_id = request.args.get('user_id')
    value = db.get(user_id) or 0
    return jsonify(counter=value)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
