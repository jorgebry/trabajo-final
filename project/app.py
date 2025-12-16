from flask import Flask, jsonify
from config import Config
from database import db
from routes.workshops import workshops_bp
from routes.registrations import registrations_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(workshops_bp)
app.register_blueprint(registrations_bp)

@app.route('/')
def index():
    return jsonify({"message": "API de Talleres de Formación Profesional"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
