from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    rol = db.Column(db.String(20), nullable=False)  


class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    lugar = db.Column(db.String(100))
    categoria = db.Column(db.String(50))


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))




@app.route('/workshops', methods=['GET'])
def get_workshops():
    workshops = Workshop.query.all()
    result = []

    for w in workshops:
        result.append({
            "id": w.id,
            "nombre": w.nombre,
            "descripcion": w.descripcion,
            "fecha": w.fecha.strftime('%Y-%m-%d'),
            "hora": w.hora.strftime('%H:%M'),
            "lugar": w.lugar,
            "categoria": w.categoria
        })

    return jsonify(result), 200


@app.route('/workshops/<int:id>', methods=['GET'])
def get_workshop(id):
    w = Workshop.query.get_or_404(id)

    return jsonify({
        "id": w.id,
        "nombre": w.nombre,
        "descripcion": w.descripcion,
        "fecha": w.fecha.strftime('%Y-%m-%d'),
        "hora": w.hora.strftime('%H:%M'),
        "lugar": w.lugar,
        "categoria": w.categoria
    }), 200


@app.route('/workshops', methods=['POST'])
def create_workshop():
    data = request.json

    workshop = Workshop(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
        hora=datetime.strptime(data['hora'], '%H:%M').time(),
        lugar=data.get('lugar'),
        categoria=data.get('categoria')
    )

    db.session.add(workshop)
    db.session.commit()

    return jsonify({"message": "Taller creado correctamente"}), 201


@app.route('/workshops/<int:id>', methods=['PUT'])
def update_workshop(id):
    workshop = Workshop.query.get_or_404(id)
    data = request.json

    workshop.nombre = data.get('nombre', workshop.nombre)
    workshop.descripcion = data.get('descripcion', workshop.descripcion)
    workshop.lugar = data.get('lugar', workshop.lugar)
    workshop.categoria = data.get('categoria', workshop.categoria)

    if 'fecha' in data:
        workshop.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()

    if 'hora' in data:
        workshop.hora = datetime.strptime(data['hora'], '%H:%M').time()

    db.session.commit()

    return jsonify({"message": "Taller actualizado"}), 200



@app.route('/workshops/<int:id>', methods=['DELETE'])
def delete_workshop(id):
    workshop = Workshop.query.get_or_404(id)

    db.session.delete(workshop)
    db.session.commit()

    return '', 204



@app.route('/workshops/<int:id>/register', methods=['POST'])
def register_workshop(id):
    data = request.json
    user_id = data.get('user_id')

   
    Workshop.query.get_or_404(id)

    registration = Registration(
        user_id=user_id,
        workshop_id=id
    )

    db.session.add(registration)
    db.session.commit()

    return jsonify({"message": "Estudiante registrado al taller"}), 201





@app.route('/')
def index():
    return jsonify({"message": "API de Talleres de Formación Profesional"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  

    app.run(debug=True)
