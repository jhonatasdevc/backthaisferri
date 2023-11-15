import conect
import hashlib
import login.gerar_token as gerar_token

# Função para realizar a consulta no banco de dados
def get_user_info(email, password):
    
    # Substitua os dados de conexão com o banco de dados pelos seus próprios
    conn = conect.get_conect()
    cursor = conn.cursor()
    
    # Executa a consulta SQL
    sql = '''
        SELECT
            JSON_BUILD_OBJECT(
                'email', u.email,
                'id', u.system_id,
                'name', u.system_name,                
                'permissions', ARRAY(SELECT permission_name FROM permissions WHERE permission_id = ANY(u.permissions)),
                'roles', u.roles
            ) AS user_info
        FROM
            userSystem u
        WHERE
            u.password = md5(%s) and u.email = %s;
            ''' 
    
    cursor.execute(sql, [password, email])
    
    row = cursor.fetchone()
    
    if row is not None:
        user_info = row[0]
        user_info = gerar_token.gerar_token(user_info)
        # Rest of your code
    else:
        # Handle the case when no user information is found
        user_info = None
    cursor.close()
    conn.close()
    
    return user_info
