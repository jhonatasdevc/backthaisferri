import conect
import login.verificar_token as verificar
from flask import jsonify
from dotenv import load_dotenv


def insert_user(token, data):
    token = verificar.verificar_token(token)
    
    if token == 'valid':
        conn = conect.get_conect()
        cursor = conn.cursor()
        
        user_name = data['user_name']
        user_email = data['user_email']
        surname = data['surname']
        user_password = data['user_password']
        date_of_birth = data['date_of_birth']
        gender = data['gender']
        cpf = data['cpf']
        user_end_street = data['user_end_street']
        user_end_number = data['user_end_number']
        user_complement = data['user_complement']

        number_phone = data['number_phone']
        number_whatsapp = data['number_whatsapp']
        number_help = data['number_help']
        
        sqlnumber = """INSERT INTO public.phone_numbers
        (number_phone, number_whatsapp, number_help)
        VALUES('%s', '%s', '%s') RETURNING phone_id;
        """ %(number_phone,number_whatsapp, number_help)
        
        
        cursor.execute(sqlnumber)

        # Obter o ID retornado
        inserted_number_id = cursor.fetchone()[0]
        try:
            # Confirmar a transação
            conn.commit()
        except:
            return jsonify({'error': 'existing phone number'}), 401


        sql = """
        INSERT INTO public.users
        (user_name, user_email, surname, password_hash, user_password, created_at, phone_id, date_of_birth, gender, cpf, user_end_street, user_end_number, user_complement, city_id)
        VALUES('%s', '%s', '%s', md5('%s'), md5('%s'), now(), %s, '%s', '%s', '%s', '%s', '%s', '%s', 0);
        """ %(user_name,user_email,surname,user_password, user_password, inserted_number_id,date_of_birth,gender,cpf,user_end_street,user_end_number,user_complement)
        
        cursor.execute(sql)
        try:
            conn.commit()
        except:
            return jsonify({'error': 'Users existing'}), 200
        
        cursor.close()
        conn.close()

        return jsonify({'accept': 'Users Registration completed successfully'}), 200
    elif token == 'time expired':
        return jsonify({'error': 'Token time expired'}), 401
    elif token == 'invalid':
        return jsonify({'error': 'Token not provided'}), 401