import conect
import login.verificar_token as verificar


def get_allusers(token, pagination, pagesize):
    token = verificar.verificar_token(token)
    offset = (pagination - 1) * pagesize
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        select user_id,
        user_name,
        user_email,
        surname, 
        created_at,
        ph.number_phone,
        ph.number_whatsapp,
        ph.number_help,
        date_of_birth,
        gender,
        cpf,
        user_end_street,
        user_end_number,
        user_complement,
        city_id
        from users us
        inner join phone_numbers ph
        on ph.phone_id = us.phone_id
        LIMIT %s
        OFFSET %s
        """
        cursor.execute(sql, (pagesize, offset))
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        data_users = []
        for row in users:   
            user_id, user_name, user_email, surname, created_at, number_phone, number_whatsapp, number_help, date_of_birth, gender, cpf, user_end_street, user_end_number, user_complement, city_id = row

            users_dict = {
                'user_id': user_id,
                'name': user_name,
                'email': user_email,
                'surname': surname,
                'created_at': created_at,
                'phone_number': {
                    'number_phone': number_phone,
                    'number_whatsapp': number_whatsapp,
                    'number_help': number_help
                },
                'date_of_birth': date_of_birth,
                'gender': gender,
                'cpf': cpf,
                'end_street': user_end_street,
                'end_number': user_end_number,
                'complement': user_complement
            }
            data_users.append(users_dict)

        # Calculate total number of pages (Assuming you have a way to get the total number of products)
        #total_products = # You need to query the database to get the total count of products
        #total_pages = (total_products + pagesize - 1) // pagesize

        result = {
            "users": data_users,
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

def get_users_id(token, user_id):
    token = verificar.verificar_token(token)
    
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        sql = """
        select user_id,
        user_name,
        user_email,
        surname, 
        created_at,
        ph.number_phone,
        ph.number_whatsapp,
        ph.number_help,
        date_of_birth,
        gender,
        cpf,
        user_end_street,
        user_end_number,
        user_complement,
        city_id
        from users us
        inner join phone_numbers ph
        on ph.phone_id = us.phone_id
        where us.user_id = %s
        """
        cursor.execute(sql, (user_id))
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        data_users = []
        for row in users:   
            user_id, user_name, user_email, surname, created_at, number_phone, number_whatsapp, number_help, date_of_birth, gender, cpf, user_end_street, user_end_number, user_complement, city_id = row

            users_dict = {
                'user_name': user_name,
                'user_email': user_email,
                'surname': surname,
                'created_at': created_at,
                'phone_number': {
                    'number_phone': number_phone,
                    'number_whatsapp': number_whatsapp,
                    'number_help': number_help
                },
                'date_of_birth': date_of_birth,
                'gender': gender,
                'cpf': cpf,
                'user_end_street': user_end_street,
                'user_end_number': user_end_number,
                'user_complement': user_complement
            }
            data_users.append(users_dict)

        # Calculate total number of pages (Assuming you have a way to get the total number of products)
        #total_products = # You need to query the database to get the total count of products
        #total_pages = (total_products + pagesize - 1) // pagesize

        result = {
            "users": data_users
        }

        return result
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')
