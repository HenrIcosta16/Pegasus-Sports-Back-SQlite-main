# from helpers.database import db
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     firebase_id = db.Column(db.String(255), nullable=True, unique=True)  # Para usuários autenticados via Google
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=True)  # Para autenticação tradicional com e-mail/senha
#     role = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.String(15), nullable=True)
#     registrationId = db.Column(db.String(255), nullable=True)

#     def __init__(self, firebase_id, name, email, password, role, phone, registrationId):
#         self.firebase_id = firebase_id
#         self.name = name
#         self.email = email
#         self.password = password
#         self.role = role
#         self.phone = phone
#         self.registrationId = registrationId

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

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'firebase_id': self.firebase_id,
#             'name': self.name,
#             'email': self.email,
#             'role': self.role,
#             'phone': self.phone,
#             'registrationId': self.registrationId
#         }

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password, password)
