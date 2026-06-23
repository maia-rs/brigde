from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.user_service import *
from schemas.user_schema import GetUser
from schemas.user_schema import CreateUser,UpdateUser # Importar o schema de criação
from schemas.user_schema import Login # Importar o schema de Login



# Carrega classe Blueprint
user_bp = Blueprint('usuario', __name__)

# Rota para criar usuários

@user_bp.route('/usuario', methods=['POST'])
#@jwt_required()
def create_user():
    try:
        # 1. Validação de entrada com Pydantic
        user_data = CreateUser.model_validate(request.get_json())
        
        # Executa as criações e buscas pelos Services
        novo_usuario = UsuarioService.create_usuario(user_data.model_dump()) # Passa o dicionário validado
        
        # 2. Resposta simplificada usando o GetUser schema
        usuario_formatado = GetUser.model_validate(novo_usuario).model_dump(mode='json')
        return jsonify({"message": "Usuário criado com sucesso", "user": usuario_formatado}), 201

    
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
           
    try:
        # 1. Validação de entrada com Pydantic
        login_data = Login.model_validate(request.get_json())
        email = login_data.email
        senha = login_data.senha

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
        print("ERRO:", str(e)) # Corrigido o print
        return jsonify({"error": "Erro interno no servidor.", "details": str(e)}), 500


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
        print("ERRO:", str(e))
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
    try:
        # 1. Validação de entrada com Pydantic
        user_data = UpdateUser.model_validate(request.get_json())

        # Chama o Service para atualizar o usuário
        usuario = UsuarioService.update_usuario(user_id, user_data.model_dump(exclude_unset=True)) # Passa o dicionário validado

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
        print("ERRO:", str(e)) # Corrigido o print
        return jsonify({"error": "Erro interno no servidor.", "details": str(e)}), 500
