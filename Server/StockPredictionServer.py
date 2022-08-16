import json

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.before_request
def check_authentication():
    print(f"checking authentication.. {request.headers['username']}")


@app.route('/predict', methods=['GET'])
def get_predict_data():
    print(f"predicting data for - {request.args}")
    return json.dumps({"data": "hi"})


if __name__ == '__main__':
    app.run()
