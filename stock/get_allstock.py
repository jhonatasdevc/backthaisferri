import conect
import login.verificar_token as verificar
import conect
from flask import jsonify

def get_stock(token):
    token = verificar.verificar_token(token)

    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        SELECT json_agg(json_build_object(
        'product_id', sk.product_id,
        'description', pd.description,
        'color', pd.color,
        'size', pd.size,
        'model_description', md.model_description,
        'quantity', sk.quantity,
        'online', pd.online
        )) AS result
        FROM stock sk
        INNER JOIN product pd ON pd.product_id = sk.product_id
        INNER JOIN model md ON md.model_id = pd.model_id;
        """
        cursor.execute(sql)
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()

        return produtos
    elif token == 'time expired':
        return jsonify({'error': 'time expired'}), 401
    elif token == 'invalid':
        return jsonify({'error': 'Login invalid'}), 401

def get_stockid(token, stock):
    token = verificar.verificar_token(token)

    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        SELECT json_agg(json_build_object(
        'product_id', sk.product_id,
        'description', pd.description,
        'color', pd.color,
        'size', pd.size,
        'model_description', md.model_description,
        'quantity', sk.quantity,
        'online', pd.online
        )) AS result
        FROM stock sk
        INNER JOIN product pd ON pd.product_id = sk.product_id
        INNER JOIN model md ON md.model_id = pd.model_id
        WHERE pd.product_id = %s;
        """

        cursor.execute(sql, str(stock))
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()

        return produtos
    elif token == 'time expired':
        return jsonify({'error': 'time expired'}), 401
    elif token == 'invalid':
        return jsonify({'error': 'Login invalid'}), 401
