import conect
import login.verificar_token as verificar
import conect

def get_product(token, pagination, pagesize):
    token = verificar.verificar_token(token)
    offset = (pagination - 1) * pagesize
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        SELECT  pd.product_id,
        pd.description,
        pd.picture,
        pd.model_id,
        md.model_description,
        pd.color,
        pd.size,
        pd.online
        FROM product pd
        INNER JOIN model md ON md.model_id = pd.model_id
        LIMIT %s
        OFFSET %s
        """
        cursor.execute(sql, (pagesize, offset))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        produtos = []
        for row in data:
            # Unpack all the row items into separate variables
            product_id, description, picture, model_id, model_description, color, size, online = row
            
            # Create a dictionary for the product with a nested dictionary for the model
            product_dict = {
                "id": product_id,
                "description": description,
                "picture": picture,
                "color": color,
                "size": size,
                "online": online,
                "model": {
                    "id": model_id,
                    "description": model_description
                }
            }
            produtos.append(product_dict)

        # Calculate total number of pages (Assuming you have a way to get the total number of products)
        #total_products = # You need to query the database to get the total count of products
        #total_pages = (total_products + pagesize - 1) // pagesize

        result = {
            "products": produtos,
            "pagination": {
                "current": pagination,
                "total": offset  # Note that total should likely be the total number of pages, not the offset
            }
        }

        return result
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')

def get_productid(token, product):
    token = verificar.verificar_token(token)

    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        SELECT pd.product_id,
        pd.description,
        pd.picture,
        pd.model_id,
        md.model_description,
        pd.color,
        pd.size,
        pd.online
        FROM product pd
        INNER JOIN model md ON md.model_id = pd.model_id
        WHERE pd.product_id = %s;
        """
        cursor.execute(sql, str(product))
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        produto = [dict(zip(col_names, row)) for row in data]
        cursor.close()
        conn.close()

        return produto
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')

def insert_product(token, product_data):
    token = verificar.verificar_token(token)

    picture_url = product_data.get('picture_url')
    model_id = product_data.get('model_id')
    color = product_data.get('color')
    size = product_data.get('size')
    description = product_data.get('description')
    online = product_data.get('online')
    
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        INSERT INTO product (picture, model_id, color, size, description, online)
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );"""

        cursor.execute(sql, [picture_url, model_id, color, size, description, online])
        conn.commit()
        cursor.close()
        conn.close()

        return "cadastro realizado"
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')

def update_product(token, product_data):
    token = verificar.verificar_token(token)

    product_id = product_data.get('product_id')
    picture_url = product_data.get('picture_url')
    model_id = product_data.get('model_id')
    color = product_data.get('color')
    size = product_data.get('size')
    online = product_data.get('online')
    description = product_data.get('description')
    
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        UPDATE public.product
        SET picture=%s, model_id=%s, color=%s, "size"=%s, online=%s, description=%s
        WHERE product_id= %s;"""

        cursor.execute(sql, [picture_url, model_id, color, size, online, description, product_id])
        conn.commit()

        sql = """
        SELECT json_agg(json_build_object(
        'product_id', pd.product_id,
        'description', pd.description,
        'picture', pd.picture,
        'model_id', pd.model_id,
        'model_description', md.model_description,
        'color', pd.color,
        'size', pd.size,
        'online', pd.online
        )) AS json_result
        FROM product pd
        INNER JOIN model md ON md.model_id = pd.model_id
        WHERE pd.product_id = %s;
        """

        cursor.execute(sql, str(product_id))
        product = cursor.fetchall()

        cursor.close()
        conn.close()

        return product
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')
