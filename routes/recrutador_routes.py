from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.recrutador_service import *
from schemas.user_schema import GetUser
from schemas.recrutador_schema import GetRecrutador
from schemas.recrutador_schema import CreateRecrutador, UpdateRecrutador # Importar schemas de criação e atualização
from services.user_service import *
from datetime import datetime



# Carrega classe Blueprint
recrutador_bp = Blueprint('recrutador', __name__)

# Rota para criar perfil recrutador
@recrutador_bp.route('/recrutador/<int:user_id>', methods=['POST'])
# @jwt_required()
def create_recrutador_perfil(user_id):
    try:
        # 1. Validação de entrada com Pydantic
        recrutador_data = CreateRecrutador.model_validate(request.get_json())
        
        # Executa as criações e buscas pelos Services
        recrutador = RecrutadorService.create_recrutador(recrutador_data.model_dump(), user_id)
        
        # Formata o recrutador usando seu schema do Pydantic
        recrutador_formatado = GetRecrutador.model_validate(recrutador).model_dump(mode='json')
        
        # Resposta simplificada
        return jsonify({"message": "Recrutador criado com sucesso", "recrutador": recrutador_formatado}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        db.session.rollback()
        print("ERRO REAL NO SERVIDOR:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
        

#Rota para consultar recrutador por ID

@recrutador_bp.route('/recrutador/<int:recrutador_id>', methods=['GET'])
#@jwt_required()
def get_recrutador_by_id(recrutador_id):
    try:
        # Chama o Service para buscar o recrutador
        recrutador = RecrutadorService.get_recrutador_by_id(recrutador_id)

        # Se o Service retornar None 
        if not recrutador:
            return jsonify({"error": "recrutador não encontrado."}), 404

        # O Pydantic valida o candidato único e converte o Enum para String com mode='json'
        recrutador_formatado = GetRecrutador.model_validate(recrutador).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Recrutador encontrado com sucesso",
            "recrutador": recrutador_formatado # Chave corrigida
        }), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback() # Corrigido o print
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500


#Listas todos os recrutadores do banco do banco
@recrutador_bp.route('/recrutador', methods=['GET'])
#@jwt_required()
def get_recrutadores():
    try:
        
        recrutadores_banco = RecrutadorService.get_recrutadores()

        if not recrutadores_banco:
            return jsonify({"message": "Nenhum recrutador cadastrado.", "recrutadores": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_recrutadores = [GetRecrutador.model_validate(u).model_dump(mode='json') for u in recrutadores_banco]
        
        # 3. Retorno 
        return jsonify({
            "message": "Rescrutador encontrados com sucesso",
            "recrutadores": lista_recrutadores # Chave corrigida
        }), 200
    
    except ValueError as e:
            #Recrutador não encontrado
            return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) # Corrigido o print
        return jsonify({"error": "Erro interno no servidor."}), 


#Busca o recrutador pelo nome
@recrutador_bp.route('/recrutador/busca_nome', methods=['GET'])
#@jwt_required()
def get_recrutador_nome():

    nome = request.args.get('nome')
 
    if not nome:
        return jsonify({"Informe o nome de um Recrutador"})



    try:
        
        recrutador = RecrutadorService.get_recrutador(nome)

        if not recrutador:
            return jsonify({"message": "Nenhum recrutador cadastrado.", "recrutador": []}), 200

    
        recrutador_formatado = GetRecrutador.model_validate(recrutador).model_dump(mode='json')
        
        # Retorno 
        return jsonify({
            "message": "Recrutador encontrados com sucesso",
            "recrutador": recrutador_formatado
        }), 200

    except ValueError as e:
            #Recrutador não encontrado
            return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500


#Busca o recrutadores por empresa
@recrutador_bp.route('/recrutador/empresa', methods=['GET'])
#@jwt_required()
def get_recrutador_empresa():

    empresa = request.args.get('empresa')
 
    if not empresa:
        return jsonify({"error": "É necessário informar o parâmetro 'empresa' na URL."}), 400



    try:
        
        recrutadores_banco= RecrutadorService.get_recrutadores_by_empresa(empresa)

        if not recrutadores_banco:
            return jsonify({"message": "Nenhum recrutador encontrado para esta empresa.", "recrutadores": []}), 200 # Mensagem mais específica

    
        recrutador_formatado = [GetRecrutador.model_validate(u).model_dump(mode='json') for u in recrutadores_banco]
        # Retorno 
        return jsonify({
            "message": "Recrutadores encontrados com sucesso",
            "recrutador": recrutador_formatado
        }), 200
    
    except ValueError as e:
        # Recruatdor não encontrado
        return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    
#Atualização

#Atualiza Informações do Recrutador
@recrutador_bp.route('/recrutador/<int:recrutador_id>', methods=['PUT'])
#@jwt_required()
def update_recrutador(recrutador_id):
    try:
        # 1. Validação de entrada com Pydantic
        recrutador_data = UpdateRecrutador.model_validate(request.get_json())
        
        # Chama o Service para atualizar o recrutador
        recrutador = RecrutadorService.update_recrutador(recrutador_id, recrutador_data.model_dump(exclude_unset=True))

        # Se o Service retornar None 
        if not recrutador:
            return jsonify({"error": "Recrutador não encontrado."}), 404
        
        # O Pydantic valida o usuário único e converte o Enum para String com mode='json'
        recrutador_formatado = GetRecrutador.model_validate(recrutador).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Recrutador atualizado com sucesso", # Mensagem mais apropriada
            "recrutador": recrutador_formatado # Chave corrigida
        }), 200
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print("ERRO:", str(e)) # Corrigido o print
        return jsonify({"error": "Erro interno no servidor.", "details": str(e)}), 500
        
        
