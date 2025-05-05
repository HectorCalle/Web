from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id =db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(200), nullable=False)
    correo =db.Column(db.String(200), unique=True nullable=False)
    contracena_hash =db.Column(db.String(256), nullable=False)
class Tarea(db.Model):
    __tablename__ = 'tareas'

    id =db.Column(db.Integer, primary_key=True)
    titulo =db.Column(db.String(200), nullable=False)
    descripcion =db.Column(db.text, nullable=False)
    fecha_creacion =db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento =db.Column(db.DateTime, nullable=False)
    completada =db.Column(db.Boolean, default=false)
    prioridad =db.column(db.String(50), nullable=false)
    usuario_id =db.Column(db.Integer, db.Foreign_key('usuarios.id'), nullable=False )
