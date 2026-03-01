import firebase_admin
from firebase_admin import credentials, auth

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate('path/to/your/firebase-admin-sdk.json')
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # Retorna o ID do usuário e outras informações
    except Exception as e:
        return None  # Caso o token seja inválido ou expirado
