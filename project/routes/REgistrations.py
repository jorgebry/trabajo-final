from flask import Blueprint, request, jsonify
from models import Registration, Workshop
from database import db

registrations_bp = Blueprint('registrations', __name__)

@registrations_bp.route('/workshops/<int:id>/register', methods=['POST'])
def register_workshop(id):
    data = request.json
    Workshop.query.get_or_404(id)

    registration = Registration(
        user_id=data['user_id'],
        workshop_id=id
    )

    db.session.add(registration)
    db.session.commit()
    return jsonify({"message": "Estudiante registrado"}), 201
