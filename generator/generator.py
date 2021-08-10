from flask import Flask, request
from random import randint
import json

# create the Flask app
app = Flask(__name__)

@app.get('/ping')
def ping():
    return 'pong'

@app.route('/', methods=['POST'])
def json_example():
    model = request.args.get('model')
    viewer = request.args.get('viewer')
    result = str(randint(0, 9))
    json_str = {
        "reason": model,
        "result": result
    }
    y = json.dumps(json_str)
    return y

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)