# Creacion de los modelos de la BD
from . import db
from flask_login import UserMixin
from datetime import datetime

# Tabla de usuarios
class User(db.Model, UserMixin):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(150), unique=True)
    password   = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avatar     = db.Column(db.String(100), default='avatar1.png')

    # Relación: un usuario tiene muchas predicciones
    predicciones = db.relationship('Prediccion', backref='usuario', lazy=True, cascade='all, delete-orphan')

# Tabla para el modelo de prediccion
class Prediccion(db.Model):
    id                     = db.Column(db.Integer, primary_key=True)
    user_id                = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre                 = db.Column(db.String(100), nullable=False)
    precio                 = db.Column(db.Float)
    edad_minima            = db.Column(db.Integer)
    mes_de_lanzamiento     = db.Column(db.Integer)
    caracteristicas_y_genero = db.Column(db.Text)
    probabilidad           = db.Column(db.Float)          # resultado % del modelo
    fecha_guardado         = db.Column(db.DateTime, default=datetime.utcnow)