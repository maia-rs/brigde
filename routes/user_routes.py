from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.banco import db
from services.user_service import *



# Carrega classe Blueprint
user_bp = Blueprint('usuario', __name__)

@user_bp.route('/usuario', methods=['POST'])
#@jwt_required()
def create_user():
    data = request.get_json() or {}
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, email, senha]):
        return jsonify({"error": "Necessário informar nome,email e senha"}), 400
    
    try:

        novo_usuario = UsuarioService.create_usuario(data)

        return jsonify(
            {"message":"usário criado com suscesso",
             "user": {
                 "id": novo_usuario.id,
                 "nome": novo_usuario.nome,
                 "email": novo_usuario.email,
                 }}),201

    
    except ValueError as e:
            # Captura erros de validação do Service (ex: e-mail duplicado)
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        return jsonify({"error": "Erro interno no servidor."}), 500