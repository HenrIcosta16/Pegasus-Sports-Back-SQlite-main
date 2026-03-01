# from flask import Blueprint, request, jsonify
# from models.PacienteM import Paciente, db


# paciente_blueprint = Blueprint('pacientes', __name__)

# # Rota para listar pacientes
# @paciente_blueprint.route('/pacientes', methods=['GET'])
# def get_pacientes():
#     try:
#         pacientes = Paciente.query.all()
#         pacientes_data = [paciente.__dict__ for paciente in pacientes]
#         for paciente in pacientes_data:
#             paciente.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal data
#         return jsonify(pacientes_data)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao obter os pacientes: {str(e)}"}), 500

# # Rota para buscar um paciente específico pelo ID
# @paciente_blueprint.route('/pacientes/<int:id>', methods=['GET'])
# def get_paciente(id):
#     try:
#         paciente = Paciente.query.get(id)
#         if not paciente:
#             return jsonify({"message": "Paciente não encontrado"}), 404
#         return jsonify(paciente.__dict__)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao obter o paciente: {str(e)}"}), 500

# # Rota para criar um novo paciente
# @paciente_blueprint.route('/pacientes', methods=['POST'])
# def create_paciente():
#     try:
#         data = request.get_json()

#         # Validação de dados obrigatórios
#         if not all(key in data for key in ['nome', 'numeroCartaoSUS', 'identidade', 'cpf']):
#             return jsonify({"message": "Dados incompletos."}), 400

#         # Verificar duplicidade de dados
#         paciente_existente = Paciente.query.filter(
#             (Paciente.numeroCartaoSUS == data['numeroCartaoSUS']) | 
#             (Paciente.identidade == data['identidade']) |
#             (Paciente.cpf == data['cpf'])
#         ).first()

#         if paciente_existente:
#             return jsonify({"message": "Paciente já cadastrado."}), 400

#         # Criar e salvar o novo paciente
#         novo_paciente = Paciente(**data)
#         novo_paciente.save()

#         return jsonify(novo_paciente.__dict__), 201
#     except Exception as e:
#         return jsonify({"message": f"Erro ao salvar o paciente: {str(e)}"}), 500

# # Rota para editar um paciente existente
# @paciente_blueprint.route('/pacientes/<int:id>', methods=['PUT'])
# def update_paciente(id):
#     try:
#         paciente = Paciente.query.get(id)
#         if not paciente:
#             return jsonify({"message": "Paciente não encontrado"}), 404

#         data = request.get_json()
#         paciente.update(data)
#         return jsonify(paciente.__dict__)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao atualizar o paciente: {str(e)}"}), 500

# # Rota para excluir um paciente
# @paciente_blueprint.route('/pacientes/<int:id>', methods=['DELETE'])
# def delete_paciente(id):
#     try:
#         paciente = Paciente.query.get(id)
#         if not paciente:
#             return jsonify({"message": "Paciente não encontrado"}), 404

#         paciente.delete()
#         return jsonify({"message": "Paciente excluído com sucesso."}), 200
#     except Exception as e:
#         return jsonify({"message": f"Erro ao excluir o paciente: {str(e)}"}), 500
