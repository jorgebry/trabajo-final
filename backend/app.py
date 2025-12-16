from flask import Flask
from routes.workshops import workshops_bp

app = Flask(__name__)
app.register_blueprint(workshops_bp)

if __name__ == '__main__':
    app.run(debug=True)
