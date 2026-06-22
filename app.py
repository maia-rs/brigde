import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from pydantic import ValidationError
from models.banco import db
# Importa os blueprints
from routes.user_routes import user_bp
from routes.candidato_routes import candidato_bp
from routes.recrutador_routes import recrutador_bp
from routes.vagas_routes import vagas_bp
from routes.candidatura_routes import candidatura_bp

load_dotenv()

app = Flask(__name__)
# Alternativa para versões mais recentes do Flask
app.json.ensure_ascii = False

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brigde.db'

jwt = JWTManager(app)
db.init_app(app)

# Registra os blueprints
app.register_blueprint(user_bp)
app.register_blueprint(candidato_bp)
app.register_blueprint(recrutador_bp)
app.register_blueprint(vagas_bp)
app.register_blueprint(candidatura_bp)

with app.app_context():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_pydantic_validation_error(e):
    return jsonify({"error": e.errors()}), 400


@app.route('/')
def hello_world():
    return 'Hello, World!'




if __name__ == '__main__':
    app.run(debug=True)
