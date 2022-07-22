from flask import Flask, request, jsonify, make_response
from json import dumps

from controllers import evaluate_product

app = Flask(__name__)

@app.route('/')
def home():
    return make_response(jsonify({'name':'Jimit', 'address':'India'}), 200)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    if request.method == 'POST':
        comments = request.json['comments']
        result = evaluate_product(comments)
        return make_response(jsonify({ 'result': result }), 200)


if __name__ == '__main__':
    app.run()
