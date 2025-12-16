from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    lugar = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
