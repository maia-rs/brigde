from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.user_service import *
from schemas.user_schema import GetUser



# Carrega classe Blueprint
user_bp = Blueprint('usuario', __name__)

# Rota para criar usuários

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
            {"message":"usuário criado com suscesso",
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
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    


# Rota para login

#Atualiza Informações do usuário   
@user_bp.route('/login', methods=['POST'])
def login():
           
    email_entrada= request.get_json() or {}
    senha_entrada= request.get_json() or {}
    email = email_entrada.get('email')
    senha = senha_entrada.get('senha')


    if not all([email,senha]):
        return jsonify({"error": "Necessário informar e-mail e senha"}), 400
    

    try:

        # Chama o Service para logar o usuário
        usuario = UsuarioService.verify_login(email,senha)

        if usuario:
            access_token = create_access_token(identity=str(usuario.id))
                          
            # O Pydantic valida o usuário único e converte o Enum para String com mode='json'
            usuario_formatado = GetUser.model_validate(usuario).model_dump(mode='json')

            # Retorno 
            return jsonify({
                "message": "Usuário logado com sucesso",
                
                "user": usuario_formatado,

                "token": access_token
                
            }), 200
    
    except ValueError as e:
            # Captura erros de validação do Service (ex: e-mail duplicado)
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        erro = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."},f'{erro}'), 500


#Rota para consultar usuário por ID

@user_bp.route('/usuario/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    try:
        # Chama o Service para buscar o usuário
        usuario = UsuarioService.get_usuario_by_id(user_id)

        # Se o Service retornar None (usuário não encontrado)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # O Pydantic valida o usuário único e converte o Enum para String com mode='json'
        usuario_formatado = GetUser.model_validate(usuario).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Usuário encontrado com sucesso",
            "user": usuario_formatado
        }), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

    
#Listas todos os usuários do banco
@user_bp.route('/usuario', methods=['GET'])
@jwt_required()
def get_users():
    try:
        
        usuarios_banco = UsuarioService.get_usuarios()

        if not usuarios_banco:
            return jsonify({"message": "Nenhum usuário cadastrado.", "users": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_usuarios = [GetUser.model_validate(u).model_dump(mode='json') for u in usuarios_banco]
        
        # 3. Retorno 
        return jsonify({
            "message": "Usuários encontrados com sucesso",
            "users": lista_usuarios
        }), 200

    except Exception as e:
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 

 #Listas todos os usuários ATIVOS do banco
@user_bp.route('/usuario/ativos', methods=['GET'])
@jwt_required()
def get_users_ativos():
    try:
        usuarios_banco = UsuarioService.listar_usuarios_ativos()

        if not usuarios_banco:
            return jsonify({"message": "Nenhum usuário cadastrado.", "users": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_usuarios = [GetUser.model_validate(u).model_dump(mode='json') for u in usuarios_banco]
        
        # Retorno 
        return jsonify({
            "message": "Usuários encontrados com sucesso",
            "users": lista_usuarios
        }), 200

    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    
 #Listas todos os usuários Inativos do banco
@user_bp.route('/usuario/inativos', methods=['GET'])
@jwt_required()
def get_users_inativos():
    try:
        
        usuarios_banco = UsuarioService.listar_usuarios_inativos()

        if not usuarios_banco:
            return jsonify({"message": "Nenhum usuário cadastrado.", "users": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_usuarios = [GetUser.model_validate(u).model_dump(mode='json') for u in usuarios_banco]
        
        # 3. Retorno 
        return jsonify({
            "message": "Usuários encontrados com sucesso",
            "users": lista_usuarios
        }), 200

    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    

 #Atualiza Informações do usuário   
@user_bp.route('/usuario/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_users(user_id):
           
    data = request.get_json() or {}
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')


    if not any([nome, email, senha]):
        return jsonify({"error": "Necessário informar dados a serem atualizados"}), 400
    

    try:

        # Chama o Service para atualizar o usuário
        usuario = UsuarioService.update_usuario(user_id,data)

        # Se o Service retornar None (usuário não encontrado)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 404
        
        # O Pydantic valida o usuário único e converte o Enum para String com mode='json'
        usuario_formatado = GetUser.model_validate(usuario).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Usuário atualizado com sucesso",
            "user": usuario_formatado
        }), 200
    
    except ValueError as e:
            # Captura erros de validação do Service (ex: e-mail duplicado)
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        erro = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."},f'{erro}'), 500
