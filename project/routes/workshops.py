from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Workshop
from database import db

workshops_bp = Blueprint('workshops', __name__)

@workshops_bp.route('/workshops', methods=['GET'])
def get_workshops():
    workshops = Workshop.query.all()
    return jsonify([
        {
            "id": w.id,
            "nombre": w.nombre,
            "descripcion": w.descripcion,
            "fecha": w.fecha.strftime('%Y-%m-%d'),
            "hora": w.hora.strftime('%H:%M'),
            "lugar": w.lugar,
            "categoria": w.categoria
        } for w in workshops
    ]), 200


@workshops_bp.route('/workshops/<int:id>', methods=['GET'])
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


@workshops_bp.route('/workshops', methods=['POST'])
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
    return jsonify({"message": "Taller creado"}), 201


@workshops_bp.route('/workshops/<int:id>', methods=['PUT'])
def update_workshop(id):
    workshop = Workshop.query.get_or_404(id)
    data = request.json

    workshop.nombre = data.get('nombre', workshop.nombre)
    workshop.descripcion = data.get('descripcion', workshop.descripcion)
    workshop.lugar = data.get('lugar', workshop.lugar)
    workshop.categoria = data.get('categoria', workshop.categoria)

    db.session.commit()
    return jsonify({"message": "Taller actualizado"}), 200


@workshops_bp.route('/workshops/<int:id>', methods=['DELETE'])
def delete_workshop(id):
    workshop = Workshop.query.get_or_404(id)
    db.session.delete(workshop)
    db.session.commit()
    return '', 204
