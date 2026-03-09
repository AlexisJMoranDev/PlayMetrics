#Creacion de los modelos de la BD
from . import db
from flask_login import UserMixin

# Tabla de usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avatar = db.Column(db.String(100), default='avatar1.png')

# Tabla para el modelo de prediccion
class Prediccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)
    edad_minima = db.Column(db.Integer)
    mes_de_lanzamiento = db.Column(db.Integer)
    caracteristicas_y_genero = db.Column(db.Text)