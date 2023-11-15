from flask import Flask, jsonify, request
from flask_cors import CORS

import login.user_info as user_info
import correios.get_address as mails

import users.get_users as users
import users.insert_user 

import stock.get_allstock as get_allstock
import product.get_product as get_allproduct
import model.get_allmodel as get_allmodel

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# Rota para o login
@app.route('/')
def home():
    return jsonify("Todes")

@app.route('/api/login', methods = ['POST'])
def login():
    if request.method == 'POST':
       data = request.get_json()
       email = data.get('email')
       password = data.get('password')
       
       if not email or not password:
            return jsonify({'message': 'Email ou senha não fornecidos.'}), 400
    
       
       user = user_info.get_user_info(email, password)
    
       if user:
            return jsonify(user)
       else:
            return jsonify({'message': 'Email ou senha incorretos.'}), 401
    
@app.route('/api/mail', methods=['GET'])   
def alladdress():
    token = request.headers.get('Authorization')
    zipcode = request.args.get('cep')
    data_mails = mails.get_address(token, zipcode)
    return data_mails

@app.route('/api/users', methods=['GET', 'POST', 'UPDATE'])
def alluser():
    if request.method  == 'GET':
        token = request.headers.get('Authorization') 
        users_id = request.args.get('id')

        if users_id is not None:
            data_user = users.get_users_id(token, users_id)
            return data_user
        else:
            pagination = request.args.get('pagination', default=1, type=int)
            pagesize = request.args.get('pagesize', default=10, type=int)
            data_users = users.get_allusers(token, pagination, pagesize)
            return data_users
    elif request.method  == 'POST':
        token = request.headers.get('Authorization') 
        data = request.get_json()
        data = users.insert_user.insert_user(token, data)

        return data
    else:
        return 'Method not allowed', 405

@app.route('/api/stock')
def allstock():
    token = request.headers.get('Authorization')
    
    stock = get_allstock.get_stock(token)
    return jsonify(stock)

@app.route('/api/stock', methods=['GET'])
def get_stock_by_id():
    token = request.headers.get('Authorization')
    stock_id = request.args.get('id')
    
    if stock_id is not None:
        stock_id = int(stock_id)
        stock = get_allstock.get_stockid(token, stock_id)
        if stock:
            return jsonify(stock)
        else:
            return jsonify({'error': 'Stock not found'}), 404
    else:
        return jsonify({'error': 'Missing stock ID'}), 400

@app.route('/api/product')
def allproduct():
    token = request.headers.get('Authorization')

    product_id = request.args.get('id')
    
    if product_id is not None:
        product_id = int(product_id)
        product = get_allproduct.get_productid(token, product_id)
        if product:
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found'}), 404
    else:
        # Receba os argumentos pagination e pagesize da consulta
        pagination = request.args.get('pagination', default=1, type=int)
        pagesize = request.args.get('pagesize', default=10, type=int)
        
        product = get_allproduct.get_product(token, pagination, pagesize)
        return jsonify(product)



@app.route('/api/product', methods=['POST'])
def post_produt():
    data = request.json
    token = request.headers.get('Authorization')

    product = get_allproduct.insert_product(token, data)
    return product

@app.route('/api/product', methods=['PUT'])
def update_product():
    data = request.json
    token = request.headers.get('Authorization')
    
    product = get_allproduct.update_product(token, data)
    return product

@app.route('/api/model')
def allmodel():
    token = request.headers.get('Authorization')

    model_id = request.args.get('id')
    
    if model_id is not None:
        model_id = int(model_id)
        model = get_allmodel.get_modelid(token, model_id)
        if model:
            return jsonify(model)
        else:
            return jsonify({'error': 'Model not found'}), 404
    else:
        # Receba os argumentos pagination e pagesize da consulta
        pagination = request.args.get('pagination', default=1, type=int)
        pagesize = request.args.get('pagesize', default=10, type=int)
        
        model = get_allmodel.get_model(token, pagination, pagesize)
        return jsonify(model)
   

@app.route('/api/model', methods=['GET'])
def get_model_by_id():
    token = request.headers.get('Authorization')
    model_id = request.args.get('id')
    
    if model_id is not None:
        model_id = int(model_id)
        model = get_allmodel.get_modelid(token, model_id)
        if model:
            return jsonify(model)
        else:
            return jsonify({'error': 'Stock not found'}), 404
    else:
        pagination = request.args.get('pagination', default=1, type=int)
        pagesize = request.args.get('pagesize', default=10, type=int)
        product = get_allmodel.get_model(token, pagination, pagesize)
        return jsonify(product)

@app.route('/api/model', methods=['POST'])
def post_model():
    data = request.json
    token = request.headers.get('Authorization')

    model = get_allmodel.insert_model(token, data)
    return model

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
