# # batchR.py

# from flask import Blueprint, request, jsonify
# from models.batchM import Batch, db
# from datetime import datetime

# batches_blueprint = Blueprint('batches', __name__)

# # Função para verificar duplicidade de número de lote
# def check_duplicates(number, lot_number):
#     batch_number = Batch.query.filter_by(number=number).first()
#     batch_lot = Batch.query.filter_by(lot_number=lot_number).first()

#     return batch_number, batch_lot

# @batches_blueprint.route('/batches', methods=['GET'])
# def get_batches():
#     try:
#         batches = Batch.query.all()
#         batches_data = [batch.__dict__ for batch in batches]
#         for batch in batches_data:
#             batch.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal data
#         return jsonify(batches_data)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao obter os lotes: {str(e)}"}), 500

# @batches_blueprint.route('/batches/<int:id>', methods=['GET'])
# def get_batch(id):
#     try:
#         batch = Batch.query.get(id)
#         if not batch:
#             return jsonify({"message": "Lote não encontrado"}), 404
#         return jsonify(batch.__dict__)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao obter o lote: {str(e)}"}), 500

# @batches_blueprint.route('/batches', methods=['POST'])
# def create_batch():
#     try:
#         data = request.get_json()

#         # Validação de dados obrigatórios
#         if not all(key in data for key in ['number', 'lot_number', 'expiration_date', 'manufacturer', 'quantity', 'medication_name', 'medication_image', 'manufacturing_date', 'grams']):
#             return jsonify({"message": "Dados incompletos."}), 400

#         batch_number, batch_lot = check_duplicates(data['number'], data['lot_number'])
#         if batch_number:
#             return jsonify({"message": "O código do lote de farmácia já existe."}), 400
#         if batch_lot:
#             return jsonify({"message": "O lote de compra já existe."}), 400

#         # Criar e salvar o lote
#         new_batch = Batch(**data)
#         new_batch.save()

#         return jsonify(new_batch.__dict__), 201
#     except Exception as e:
#         return jsonify({"message": f"Erro ao salvar o lote: {str(e)}"}), 500

# @batches_blueprint.route('/batches/<int:id>', methods=['PUT'])
# def update_batch(id):
#     try:
#         batch = Batch.query.get(id)
#         if not batch:
#             return jsonify({"message": "Lote não encontrado"}), 404

#         data = request.get_json()
        
#         batch_number, batch_lot = check_duplicates(data['number'], data['lot_number'])
#         if batch_number and batch_number.id != id:
#             return jsonify({"message": "O código do lote de farmácia já existe."}), 400
#         if batch_lot and batch_lot.id != id:
#             return jsonify({"message": "O lote de compra já existe."}), 400

#         batch.update(data)
#         return jsonify(batch.__dict__)
#     except Exception as e:
#         return jsonify({"message": f"Erro ao atualizar o lote: {str(e)}"}), 500

# @batches_blueprint.route('/batches/<int:id>', methods=['DELETE'])
# def delete_batch(id):
#     try:
#         batch = Batch.query.get(id)
#         if not batch:
#             return jsonify({"message": "Lote não encontrado"}), 404

#         batch.delete()
#         return jsonify({"message": "Lote excluído com sucesso."}), 200
#     except Exception as e:
#         return jsonify({"message": f"Erro ao excluir o lote: {str(e)}"}), 500
