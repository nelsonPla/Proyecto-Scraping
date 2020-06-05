from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime





app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonmongodb'
mongo = PyMongo(app)

@app.route('/notis', methods=['GET'])
def get_prueba():
    url = 'https://www.lapagina.com.sv/'
    page = requests.get(url)
    
    #print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    
    #encabezado de noticia
    ec = soup.find_all('h3', class_='jeg_post_title')
    titulos = list()
    for i in ec:
        titulos.append(i.text)
    
    #Autor de la noticia
    by = soup.find_all('div', class_='jeg_meta_author')
    autor = list()
    for i in by:
        autor.append(i.a.text)
    
    #texto de noticia
    contenedor = soup.find_all('div', class_='jeg_post_excerpt')
    textou = list()
    for i in contenedor:
        textou.append(i.p.text)
    
    #imagenes de noticia
    img = soup.find_all('img', class_='wp-post-image')
    imagen = list()
    for i in img:
        imagen.append(i['data-src'])
    
    #hora
    now = datetime.now()
    fecha = now.year + now.month + now.day
    
    #guardar en la base de datos
    s = 0
    for i in titulos:
        id = mongo.db.notis.insert(
            {'titulo': titulos[s], 'autor': autor[s], 'text': textou[s], 'imagen': imagen[s], 'fecha': fecha}
        )
        s = s + 1
    return {'message': 'Noticias guardadas'}

@app.route('/usuario', methods=['POST'])
def insert_usuario():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if username and password and email:
        id = mongo.db.usuar.insert(
            {'username': username, 'email': email, 'password': password}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': password,
            'email': email
        }
        return response
    else:
        return not_found()
    return {'message': 'enviado'}

@app.route('/usuarios', methods=['POST'])
def get_user():
    username = request.json['username']
    password = request.json['password']


    print(username)

    if username and password:
        user = mongo.db.usuar.find(
           {'username': username, 'password': password}
        )
        return {'message': 'usuario encontrado'} 
    else:
        return {'message': 'Usuario o contraseña esta vacio'}

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

@app.route('/noticias', methods=['GET'])
def get_noticias():
    noticias = mongo.db.news.find()
    response = json_util.dumps(noticias)
    return Response(response, mimetype='application/json')

@app.route('/noticias/<titulo>', methods=['GET'])
def get_noticia(titulo):
    noticia = mongo.db.news.find(titulo)
    response = json_util.dumps(noticia)
    return Response(response, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)