# models/agendamento.py
from datetime import datetime
from helpers.database import db  # Importar do helpers.database

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.String(255), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    veiculo = db.Column(db.String(255), nullable=False)
    servico = db.Column(db.String(255), nullable=False)
    dataPreferencial = db.Column(db.String(10), nullable=True)
    dataFormatada = db.Column(db.String(255), nullable=True)
    horarioPreferencial = db.Column(db.String(5), nullable=True)
    mensagem = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')

    def __init__(self, nome, telefone, email, veiculo, servico, dataPreferencial, dataFormatada, 
                 horarioPreferencial, mensagem, timestamp, status):
        self.id = f"local-{int(datetime.utcnow().timestamp())}"
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.veiculo = veiculo
        self.servico = servico
        self.dataPreferencial = dataPreferencial
        self.dataFormatada = dataFormatada
        self.horarioPreferencial = horarioPreferencial
        self.mensagem = mensagem
        self.timestamp = timestamp
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()