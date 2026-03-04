#Creacion de los modelos de la BD
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #ID de la nota
    data = db.Column(db.String(10000)) #Contenido de la nota
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #Fecha de creacion de la nota
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #ID del usuario al que pertenece la nota


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #ID del usuario
    email = db.Column(db.String(150), unique=True) #Correo del usuario
    password = db.Column(db.String(150)) #Contraseña del usuario
    first_name = db.Column(db.String(150)) #Primer nombre del usuario
    avatar = db.Column(db.String(100), default='avatar1.png')
    # Nota: estaria cool agregar mas datos.
    notes = db.relationship('Note') #Relación entre el usuario y sus notas