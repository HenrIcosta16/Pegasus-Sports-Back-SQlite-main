# from flask import Blueprint, request, jsonify
# from models.userM import User  # Importando o modelo User
# from werkzeug.security import check_password_hash
# from helpers.database import db
# from datetime import datetime

# # Criando o Blueprint para os recursos de usuário
# user_blueprint = Blueprint('users', __name__)

# # Rota para cadastrar um novo usuário
# @user_blueprint.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()

#     # Verifica se os campos obrigatórios foram fornecidos
#     if not all(key in data for key in ['name', 'email', 'password', 'role', 'phone', 'registrationId']):
#         return jsonify({"message": "Dados incompletos."}), 400

#     # Verifica se o e-mail já está cadastrado
#     existing_user = User.query.filter_by(email=data['email']).first()
#     if existing_user:
#         return jsonify({"message": "Email já registrado."}), 400

#     # Criação do novo usuário
#     new_user = User(
#         firebase_id=data.get('firebase_id'),  # Para casos de login via Google (pode ser None)
#         name=data['name'],
#         email=data['email'],
#         role=data['role'],
#         phone=data['phone'],
#         registrationId=data['registrationId']
#     )

#     # Se for um cadastro com senha (não via Google), setamos a senha
#     if 'password' in data:
#         new_user.set_password(data['password'])

#     try:
#         new_user.save()
#         return jsonify(new_user.to_dict()), 201
#     except Exception as e:
#         return jsonify({"message": f"Erro ao registrar usuário: {str(e)}"}), 500


# # Rota para login de usuário (verificação de senha)
# @user_blueprint.route('/users/login', methods=['POST'])
# def login_user():
#     data = request.get_json()

#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"message": "Email e senha são obrigatórios."}), 400

#     user = User.query.filter_by(email=email).first()
    
#     if not user:
#         return jsonify({"message": "Usuário não encontrado."}), 404

#     # Verifica se a senha está correta
#     if user.password and not user.check_password(password):
#         return jsonify({"message": "Senha incorreta."}), 400

#     # Se o login for bem-sucedido, retorna os dados do usuário
#     return jsonify({
#         "message": "Login bem-sucedido",
#         "user": user.to_dict(),
#         "token": "fake-jwt-token"  # Em produção, gerar um token real
#     }), 200


# # Rota para buscar um usuário específico pelo ID
# @user_blueprint.route('/users/<int:id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get(id)
    
#     if not user:
#         return jsonify({"message": "Usuário não encontrado."}), 404

#     return jsonify(user.to_dict()), 200


# # Rota para atualizar os dados de um usuário (somente campos não relacionados ao login)
# @user_blueprint.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     data = request.get_json()

#     user = User.query.get(id)
    
#     if not user:
#         return jsonify({"message": "Usuário não encontrado."}), 404

#     # Atualiza apenas os campos fornecidos
#     user.update(data)

#     return jsonify(user.to_dict()), 200


# # Rota para excluir um usuário
# @user_blueprint.route('/users/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get(id)

#     if not user:
#         return jsonify({"message": "Usuário não encontrado."}), 404

#     user.delete()

#     return jsonify({"message": "Usuário excluído com sucesso."}), 200


# # Rota para verificar se o email já está registrado (usado no cadastro)
# @user_blueprint.route('/users/check_email', methods=['GET'])
# def check_email():
#     email = request.args.get('email')

#     if not email:
#         return jsonify({"message": "Email não fornecido."}), 400

#     # Verifica se o email já está registrado
#     user = User.query.filter_by(email=email).first()

#     if user:
#         return jsonify({"message": "Email já registrado."}), 400

#     return jsonify({"message": "Email disponível."}), 200


# # Rota de login com Google - Callback
# @user_blueprint.route('/auth/google/callback', methods=['POST'])
# def google_auth_callback():
#     google_token = request.headers.get('Authorization').split(' ')[1]

#     if not google_token:
#         return jsonify({"message": "Token não fornecido."}), 400

#     # Aqui você precisaria usar a biblioteca Firebase Admin SDK para verificar o token
#     # e obter as informações do usuário a partir do Google
#     # O código real dependeria da implementação do Firebase para fazer a verificação do token

#     # Supondo que o Firebase verifique com sucesso e retorne as informações do usuário
#     firebase_user = {
#         "id": "google-firebase-id",  # ID do usuário no Firebase
#         "name": "Nome do Usuário",
#         "email": "usuario@dominio.com",
#         "role": "farmaceutico",  # Defina o papel conforme o caso
#     }

#     # Verifica se o usuário já existe
#     user = User.query.filter_by(firebase_id=firebase_user["id"]).first()

#     if not user:
#         # Se não existir, cria o usuário
#         user = User(
#             firebase_id=firebase_user["id"],
#             name=firebase_user["name"],
#             email=firebase_user["email"],
#             role=firebase_user["role"],
#             phone="",
#             registrationId=""
#         )
#         db.session.add(user)
#         db.session.commit()

#     # Retorna o token JWT para o usuário (isso é simulado aqui)
#     return jsonify({"token": "fake-jwt-token"}), 200
