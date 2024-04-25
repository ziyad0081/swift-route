from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#This file will contain the api needed to connect the path finding algorithms to the front end , don't worry about it.

if __name__ == '__main__':
    app.run()
