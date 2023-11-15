import os
from dotenv import load_dotenv
import jwt

def verificar_token(token):
    token = token.replace("Bearer ", "")
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')

    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return "valid"
    except jwt.ExpiredSignatureError:
        return "time expired"
    except jwt.InvalidTokenError:
        return "invalid"