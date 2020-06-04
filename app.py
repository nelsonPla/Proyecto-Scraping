from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonmongodb'
mongo = PyMongo(app)



if __name__ == "__main__":
    app.run(debug=True)