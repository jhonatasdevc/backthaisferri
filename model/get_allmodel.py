import conect
import login.verificar_token as verificar
import conect

def get_model(token, pagination, pagesize):
    token = verificar.verificar_token(token)
    offset = (pagination - 1) * pagesize
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        select model_id, model_description
        from model"""
        cursor.execute(sql, (pagesize, offset))
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        model = [dict(zip(col_names, row)) for row in data]
        
        cursor.close()
        conn.close()
        
        result = {
            "model": model,
            "pagination": {
                "current": pagination,
                "total": offset
            }
        }
        
        return result
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')

def get_modelid(token, product):
    token = verificar.verificar_token(token)

    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        select json_agg(json_build_object(
        'model_id', md.model_id, 
        'model_description', md.model_description
        )) AS json_result
        from model md where md.model_id = %s"""

        cursor.execute(sql, str(product))
        models = cursor.fetchall()
        cursor.close()
        conn.close()

        return models
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')

def insert_model(token, model_data):
    token = verificar.verificar_token(token)

    model_description = model_data.get('model_description')
    
    
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        INSERT INTO model (model_description)
        VALUES (
            %s          
        );"""

        cursor.execute(sql, [model_description])
        conn.commit()
        cursor.close()
        conn.close()

        return "modelo cadastrado com sucesso!"
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')