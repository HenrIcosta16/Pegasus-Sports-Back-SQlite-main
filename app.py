from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Configuração CORS completa
CORS(app, 
     origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=True)

# Banco de dados em memória
agendamentos = []
HORARIOS = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]

@app.route('/agendamentos', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/agendamentos/', methods=['GET', 'POST', 'OPTIONS'])
def handle_agendamentos():
    """Endpoint para listar e criar agendamentos"""
    
    # Tratar preflight OPTIONS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', request.origin or '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200
    
    # GET - Listar todos os agendamentos
    if request.method == 'GET':
        try:
            # Formatar agendamentos para resposta
            agendamentos_formatados = []
            for a in agendamentos:
                data_obj = datetime.strptime(a['dataPreferencial'], '%Y-%m-%d')
                a_formatado = a.copy()
                a_formatado['dataFormatada'] = data_obj.strftime('%d/%m/%Y')
                agendamentos_formatados.append(a_formatado)
            
            return jsonify({
                'success': True,
                'agendamentos': agendamentos_formatados
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    # POST - Criar novo agendamento
    if request.method == 'POST':
        try:
            dados = request.get_json()
            
            # Validar campos obrigatórios
            campos_obrigatorios = ['nome', 'telefone', 'email', 'veiculo', 'servico', 'dataPreferencial', 'horarioPreferencial']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return jsonify({
                        'success': False,
                        'message': f'Campo {campo} é obrigatório'
                    }), 400
            
            # Verificar disponibilidade do horário
            data_horario = f"{dados['horarioPreferencial']}-{dados['dataPreferencial']}"
            conflitos = [a for a in agendamentos if a.get('id', '').startswith(data_horario)]
            
            if len(conflitos) >= 3:
                return jsonify({
                    'success': False,
                    'message': 'Horário não possui mais vagas disponíveis'
                }), 400
            
            # Criar novo agendamento
            novo_agendamento = {
                'id': f"{data_horario}-{str(uuid.uuid4())[:8]}",
                'nome': dados['nome'],
                'telefone': dados['telefone'],
                'email': dados['email'],
                'veiculo': dados['veiculo'],
                'servico': dados['servico'],
                'dataPreferencial': dados['dataPreferencial'],
                'horarioPreferencial': dados['horarioPreferencial'],
                'mensagem': dados.get('mensagem', ''),
                'timestamp': datetime.now().isoformat(),
                'status': 'pendente'
            }
            
            agendamentos.append(novo_agendamento)
            
            # Formatar data para resposta
            data_obj = datetime.strptime(novo_agendamento['dataPreferencial'], '%Y-%m-%d')
            agendamento_resposta = novo_agendamento.copy()
            agendamento_resposta['dataFormatada'] = data_obj.strftime('%d/%m/%Y')
            
            return jsonify({
                'success': True,
                'message': 'Agendamento criado com sucesso',
                'agendamento': agendamento_resposta
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }), 500

@app.route('/agendamentos/horarios-disponiveis/<data>', methods=['GET', 'OPTIONS'])
def horarios_disponiveis(data):
    """Endpoint para verificar horários disponíveis em uma data"""
    
    # Tratar preflight OPTIONS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', request.origin or '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response, 200
    
    try:
        # Validar formato da data
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        
        # Contar agendamentos por horário
        horarios_disponiveis = []
        for horario in HORARIOS:
            data_horario = f"{horario}-{data}"
            agendamentos_no_horario = [a for a in agendamentos if a.get('id', '').startswith(data_horario)]
            vagas_ocupadas = len(agendamentos_no_horario)
            vagas_restantes = max(0, 3 - vagas_ocupadas)
            
            horarios_disponiveis.append({
                'horario': horario,
                'disponivel': vagas_restantes > 0,
                'vagas_restantes': vagas_restantes
            })
        
        return jsonify(horarios_disponiveis), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/agendamentos/<id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def handle_agendamento(id):
    """Endpoint para operações em um agendamento específico"""
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', request.origin or '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        return response, 200
    
    # Buscar agendamento
    agendamento = next((a for a in agendamentos if a.get('id') == id), None)
    
    if not agendamento:
        return jsonify({
            'success': False,
            'message': 'Agendamento não encontrado'
        }), 404
    
    if request.method == 'GET':
        data_obj = datetime.strptime(agendamento['dataPreferencial'], '%Y-%m-%d')
        agendamento_resposta = agendamento.copy()
        agendamento_resposta['dataFormatada'] = data_obj.strftime('%d/%m/%Y')
        return jsonify(agendamento_resposta), 200
    
    elif request.method == 'PUT':
        dados = request.get_json()
        agendamento.update({
            'status': dados.get('status', agendamento['status']),
            'mensagem': dados.get('mensagem', agendamento['mensagem'])
        })
        return jsonify({
            'success': True,
            'message': 'Agendamento atualizado',
            'agendamento': agendamento
        }), 200
    
    elif request.method == 'DELETE':
        agendamentos.remove(agendamento)
        return jsonify({
            'success': True,
            'message': 'Agendamento removido'
        }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'message': 'API de Agendamentos',
        'endpoints': [
            'GET /agendamentos - Listar agendamentos',
            'POST /agendamentos - Criar agendamento',
            'GET /agendamentos/horarios-disponiveis/<data> - Ver horários disponíveis',
            'GET /agendamentos/<id> - Detalhes do agendamento',
            'PUT /agendamentos/<id> - Atualizar agendamento',
            'DELETE /agendamentos/<id> - Remover agendamento'
        ]
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Servidor iniciado!")
    print("📝 API disponível em: http://localhost:5000")
    print("🔧 Endpoints:")
    print("   - GET  /")
    print("   - GET  /agendamentos")
    print("   - POST /agendamentos")
    print("   - GET  /agendamentos/horarios-disponiveis/<data>")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)