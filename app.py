from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)


def get_db():
    return sqlite3.connect("workshops.db")

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            category TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            workshop_id INTEGER
        )
    """)
    db.commit()

init_db()


@app.route("/workshops", methods=["GET"])
def get_workshops():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM workshops")
    data = cursor.fetchall()
    return jsonify(data), 200

@app.route("/workshops/<int:id>", methods=["GET"])
def get_workshop(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM workshops WHERE id=?", (id,))
    workshop = cursor.fetchone()
    if workshop:
        return jsonify(workshop), 200
    return jsonify({"error": "Taller no encontrado"}), 404

@app.route("/workshops", methods=["POST"])
def create_workshop():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO workshops (name, description, date, time, location, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["name"], data["description"], data["date"],
        data["time"], data["location"], data["category"]
    ))
    db.commit()
    return jsonify({"message": "Taller creado"}), 201

@app.route("/workshops/<int:id>", methods=["PUT"])
def update_workshop(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE workshops SET
        name=?, description=?, date=?, time=?, location=?, category=?
        WHERE id=?
    """, (
        data["name"], data["description"], data["date"],
        data["time"], data["location"], data["category"], id
    ))
    db.commit()
    return jsonify({"message": "Taller actualizado"}), 200

@app.route("/workshops/<int:id>", methods=["DELETE"])
def delete_workshop(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM workshops WHERE id=?", (id,))
    db.commit()
    return jsonify({"message": "Taller eliminado"}), 200

@app.route("/workshops/<int:id>/register", methods=["POST"])
def register_student(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO registrations (student_name, workshop_id)
        VALUES (?, ?)
    """, (data["student_name"], id))
    db.commit()
    return jsonify({"message": "Registro exitoso"}), 200


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Gestión de Talleres</title>
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">

<h2 class="mb-3">📚 Talleres Disponibles</h2>
<table class="table table-bordered">
<tr><th>Nombre</th><th>Fecha</th><th>Lugar</th></tr>
{% for w in workshops %}
<tr>
<td>{{w[1]}}</td>
<td>{{w[3]}} {{w[4]}}</td>
<td>{{w[5]}}</td>
</tr>
{% endfor %}
</table>

<hr>

<h3>📝 Registrar Estudiante</h3>
<form method="post" action="/register">
<input class="form-control mb-2" name="student" placeholder="Nombre del estudiante">
<input class="form-control mb-2" name="workshop_id" placeholder="ID del taller">
<button class="btn btn-primary">Registrar</button>
</form>

<hr>

<h3>🛠️ Panel Administrador</h3>
<form method="post" action="/admin">
<input class="form-control mb-2" name="name" placeholder="Nombre">
<input class="form-control mb-2" name="description" placeholder="Descripción">
<input class="form-control mb-2" name="date" placeholder="Fecha">
<input class="form-control mb-2" name="time" placeholder="Hora">
<input class="form-control mb-2" name="location" placeholder="Lugar">
<input class="form-control mb-2" name="category" placeholder="Categoría">
<button class="btn btn-success">Crear Taller</button>
</form>

</body>
</html>
"""

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM workshops")
    workshops = cursor.fetchall()
    return render_template_string(HTML, workshops=workshops)

@app.route("/register", methods=["POST"])
def register_web():
    student = request.form["student"]
    workshop_id = request.form["workshop_id"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO registrations (student_name, workshop_id) VALUES (?, ?)",
        (student, workshop_id)
    )
    db.commit()
    return "Registro exitoso"

@app.route("/admin", methods=["POST"])
def admin_web():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO workshops (name, description, date, time, location, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["description"],
        request.form["date"],
        request.form["time"],
        request.form["location"],
        request.form["category"]
    ))
    db.commit()
    return "Taller creado"


if __name__ == "__main__":
    app.run(debug=True)
