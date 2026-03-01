# from flask_sqlalchemy import SQLAlchemy
# import time

# db = SQLAlchemy()

# class Paciente(db.Model):
#     __tablename__ = 'pacientes'

#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(255), nullable=False)
#     numeroCartaoSUS = db.Column(db.String(15), nullable=False, unique=True)
#     identidade = db.Column(db.String(10), nullable=False, unique=True)
#     cpf = db.Column(db.String(11), nullable=False, unique=True)
#     telefone = db.Column(db.String(15), nullable=True)
#     endereco = db.Column(db.String(255), nullable=True)

#     def __init__(self, nome, numeroCartaoSUS, identidade, cpf, telefone, endereco):
#         self.nome = nome
#         self.numeroCartaoSUS = numeroCartaoSUS
#         self.identidade = identidade
#         self.cpf = cpf
#         self.telefone = telefone
#         self.endereco = endereco

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def update(self, data):
#         for key, value in data.items():
#             setattr(self, key, value)
#         db.session.commit()

