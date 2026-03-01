# resourcers/agendamentoR.py
from flask import Blueprint, request, jsonify
from models.agendamento import Agendamento
from helpers.database import db  # Importar do helpers.database
from datetime import datetime
import traceback

agendamentos_blueprint = Blueprint('agendamentos', __name__)

@agendamentos_blueprint.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    try:
        print("📥 GET /agendamentos - Buscando todos agendamentos")
        agendamentos = Agendamento.query.all()
        print(f"📊 Encontrados {len(agendamentos)} agendamentos")
        
        agendamentos_data = []
        for agendamento in agendamentos:
            agendamento_dict = {
                'id': agendamento.id,
                'nome': agendamento.nome,
                'telefone': agendamento.telefone,
                'email': agendamento.email,
                'veiculo': agendamento.veiculo,
                'servico': agendamento.servico,
                'dataPreferencial': agendamento.dataPreferencial,
                'dataFormatada': agendamento.dataFormatada,
                'horarioPreferencial': agendamento.horarioPreferencial,
                'mensagem': agendamento.mensagem,
                'timestamp': agendamento.timestamp,
                'status': agendamento.status
            }
            agendamentos_data.append(agendamento_dict)
        
        return jsonify(agendamentos_data), 200
    except Exception as e:
        print(f"❌ Erro em GET /agendamentos: {str(e)}")
        traceback.print_exc()
        return jsonify({"message": f"Erro ao obter os agendamentos: {str(e)}"}), 500

@agendamentos_blueprint.route('/agendamentos/<string:id>', methods=['GET'])
def get_agendamento(id):
    try:
        print(f"📥 GET /agendamentos/{id}")
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        agendamento_dict = {
            'id': agendamento.id,
            'nome': agendamento.nome,
            'telefone': agendamento.telefone,
            'email': agendamento.email,
            'veiculo': agendamento.veiculo,
            'servico': agendamento.servico,
            'dataPreferencial': agendamento.dataPreferencial,
            'dataFormatada': agendamento.dataFormatada,
            'horarioPreferencial': agendamento.horarioPreferencial,
            'mensagem': agendamento.mensagem,
            'timestamp': agendamento.timestamp,
            'status': agendamento.status
        }
        return jsonify(agendamento_dict), 200
    except Exception as e:
        print(f"❌ Erro em GET /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao obter o agendamento: {str(e)}"}), 500

@agendamentos_blueprint.route('/horarios-disponiveis/<data>', methods=['GET'])
def get_horarios_disponiveis(data):
    try:
        print(f"📥 GET /horarios-disponiveis/{data}")
        
        # Validar formato da data
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
        
        todos_horarios = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00']
        limite_por_horario = 3
        
        horarios_disponiveis = []
        
        for horario in todos_horarios:
            agendamentos_no_horario = Agendamento.query.filter_by(
                dataPreferencial=data, 
                horarioPreferencial=horario
            ).count()
            
            disponivel = agendamentos_no_horario < limite_por_horario
            
            horarios_disponiveis.append({
                'id': f"{horario}-{data}",
                'horario': horario,
                'disponivel': disponivel,
                'vagas_restantes': max(0, limite_por_horario - agendamentos_no_horario)
            })
        
        print(f"✅ Horários para {data}: {horarios_disponiveis}")
        return jsonify(horarios_disponiveis), 200
        
    except Exception as e:
        print(f"❌ Erro em GET /horarios-disponiveis: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@agendamentos_blueprint.route('/agendamentos', methods=['POST'])
def create_agendamento():
    try:
        print("📥 POST /agendamentos - Recebendo dados")
        data = request.get_json()
        print(f"📦 Dados recebidos: {data}")
        
        # Validar campos obrigatórios
        required_fields = ['nome', 'telefone', 'email', 'veiculo', 'servico', 'dataPreferencial', 'horarioPreferencial']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Campos faltando: {missing_fields}")
            return jsonify({
                "message": f"Dados incompletos. Campos faltando: {', '.join(missing_fields)}"
            }), 400
        
        # Verificar disponibilidade
        print(f"🔍 Verificando disponibilidade para {data['dataPreferencial']} às {data['horarioPreferencial']}")
        limite_por_horario = 3
        agendamentos_no_horario = Agendamento.query.filter_by(
            dataPreferencial=data['dataPreferencial'],
            horarioPreferencial=data['horarioPreferencial']
        ).count()
        
        if agendamentos_no_horario >= limite_por_horario:
            print(f"❌ Horário lotado: {agendamentos_no_horario}/{limite_por_horario}")
            return jsonify({
                "message": f"Horário {data['horarioPreferencial']} não está mais disponível. Limite de {limite_por_horario} agendamentos atingido."
            }), 400
        
        # Formatar data para exibição
        data_formatada = data.get('dataFormatada')
        if not data_formatada and data.get('dataPreferencial'):
            try:
                data_obj = datetime.strptime(data['dataPreferencial'], '%Y-%m-%d')
                data_formatada = data_obj.strftime('%d/%m/%Y')
            except:
                data_formatada = data['dataPreferencial']
        
        # Criar novo agendamento
        print("📝 Criando novo agendamento...")
        new_agendamento = Agendamento(
            nome=data['nome'],
            telefone=data['telefone'],
            email=data['email'],
            veiculo=data['veiculo'],
            servico=data['servico'],
            dataPreferencial=data['dataPreferencial'],
            dataFormatada=data_formatada,
            horarioPreferencial=data['horarioPreferencial'],
            mensagem=data.get('mensagem', ''),
            timestamp=datetime.utcnow().isoformat(),
            status='pendente'
        )
        
        # Salvar no banco
        new_agendamento.save()
        print(f"✅ Agendamento salvo com ID: {new_agendamento.id}")
        
        # Preparar resposta
        agendamento_dict = {
            'id': new_agendamento.id,
            'nome': new_agendamento.nome,
            'telefone': new_agendamento.telefone,
            'email': new_agendamento.email,
            'veiculo': new_agendamento.veiculo,
            'servico': new_agendamento.servico,
            'dataPreferencial': new_agendamento.dataPreferencial,
            'dataFormatada': new_agendamento.dataFormatada,
            'horarioPreferencial': new_agendamento.horarioPreferencial,
            'mensagem': new_agendamento.mensagem,
            'timestamp': new_agendamento.timestamp,
            'status': new_agendamento.status
        }
        
        return jsonify({
            "message": "Agendamento criado com sucesso!",
            "agendamento": agendamento_dict
        }), 201
        
    except Exception as e:
        print(f"❌ Erro em POST /agendamentos: {str(e)}")
        traceback.print_exc()
        return jsonify({"message": f"Erro ao salvar o agendamento: {str(e)}"}), 500

@agendamentos_blueprint.route('/agendamentos/<string:id>', methods=['PUT'])
def update_agendamento(id):
    try:
        print(f"📥 PUT /agendamentos/{id}")
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        data = request.get_json()
        print(f"📦 Dados para atualização: {data}")
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(agendamento, key):
                setattr(agendamento, key, value)
        
        db.session.commit()
        print(f"✅ Agendamento {id} atualizado")
        
        agendamento_dict = {
            'id': agendamento.id,
            'nome': agendamento.nome,
            'telefone': agendamento.telefone,
            'email': agendamento.email,
            'veiculo': agendamento.veiculo,
            'servico': agendamento.servico,
            'dataPreferencial': agendamento.dataPreferencial,
            'dataFormatada': agendamento.dataFormatada,
            'horarioPreferencial': agendamento.horarioPreferencial,
            'mensagem': agendamento.mensagem,
            'timestamp': agendamento.timestamp,
            'status': agendamento.status
        }
        
        return jsonify(agendamento_dict), 200
        
    except Exception as e:
        print(f"❌ Erro em PUT /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao atualizar o agendamento: {str(e)}"}), 500

@agendamentos_blueprint.route('/agendamentos/<string:id>', methods=['DELETE'])
def delete_agendamento(id):
    try:
        print(f"📥 DELETE /agendamentos/{id}")
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        agendamento.delete()
        print(f"✅ Agendamento {id} excluído")
        
        return jsonify({"message": "Agendamento excluído com sucesso."}), 200
        
    except Exception as e:
        print(f"❌ Erro em DELETE /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao excluir o agendamento: {str(e)}"}), 500