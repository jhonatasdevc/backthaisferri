import requests
import login.verificar_token as verificar

def get_address(token, cep):
    base_url = "https://viacep.com.br/ws"
    
    token = verificar.verificar_token(token)
    
    if token == 'valid':
        url = f"{base_url}/{cep}/json/"
        response = requests.get(url)
    
        if response.status_code == 200:
            # Parse the response JSON content
            data = response.json()
            
            result = {
                'zip_code':data['cep'],
                'end_street': data['logradouro'],
                'complement':data['complemento'],
                'neighborhood':data['bairro'],
                'city':data['localidade'],
                'state':data['uf']
            }
            return result
        else:
            print(f"Error fetching data: HTTP {response.status_code}")
    elif token == 'time expired':
        print('tempo expirado')
    elif token == 'invalid':
        print('invalid token')