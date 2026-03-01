# from flask_sqlalchemy import SQLAlchemy
# import time


# db = SQLAlchemy()

# class Batch(db.Model):
#     __tablename__ = 'batches'

#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.String(12), nullable=False, unique=True)
#     lot_number = db.Column(db.String(12), nullable=False, unique=True)
#     expiration_date = db.Column(db.String(10), nullable=False)
#     manufacturer = db.Column(db.String(255), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False, default=0)
#     medication_name = db.Column(db.String(255), nullable=False)
#     medication_image = db.Column(db.Text, nullable=True)
#     manufacturing_date = db.Column(db.String(10), nullable=False)
#     grams = db.Column(db.Float, nullable=False, default=0.0)
#     unique_farmacy_lot_id = db.Column(db.String(255), nullable=False)
#     unique_purchase_lot_id = db.Column(db.String(255), nullable=False)

#     def __init__(self, number, lot_number, expiration_date, manufacturer, quantity,
#                  medication_name, medication_image, manufacturing_date, grams):
#         self.number = number
#         self.lot_number = lot_number
#         self.expiration_date = expiration_date
#         self.manufacturer = manufacturer
#         self.quantity = quantity
#         self.medication_name = medication_name
#         self.medication_image = medication_image
#         self.manufacturing_date = manufacturing_date
#         self.grams = grams
#         self.unique_farmacy_lot_id = f"{number}_{int(time.time())}"
#         self.unique_purchase_lot_id = f"{lot_number}_{int(time.time())}"
    
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

