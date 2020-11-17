from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/api.json')
def api():
    return jsonify({'value': 'Hello World'})


