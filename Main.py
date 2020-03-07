from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

#For Activating?
app = Flask(__name__)
#Believe this is to apply CORS
CORS(app)

@app.route('/')
def greeting():
    return 'Welcome to our Sales App'

