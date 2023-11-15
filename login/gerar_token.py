import jwt
import datetime
import os
from dotenv import load_dotenv

def gerar_token(user_info):
    # Chave secreta para assinar e verificar o token (mantenha isso seguro!)
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Dados para incluir no token
    payload = {
        'user_id': user_info['id'],
        'username': user_info['name'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  #Define a expiração do token para 1 hora a partir de agora
    }

    # Criar um token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    user_info['token'] = token
    
    return user_info

