from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.candidato_service import *
from schemas.user_schema import GetUser
from schemas.candidato_schema import GetCandidato
from services.user_service import *



# Carrega classe Blueprint
candidato_bp = Blueprint('candidato', __name__)

# Rota corrigida: Removemos o <int:user_id> da URL para simplificar o POST
@candidato_bp.route('/candidato/<int:user_id>', methods=['POST'])
# @jwt_required()
def create_candidato_perfil(user_id):
    data = request.get_json() or {}
    
    # Corrigido o nome da chave para buscar do JSON
    cidade = data.get('cidade')
    uf = data.get('uf')
    telefone = data.get('telefone')
    palavra_chave = data.get('palavra_chave')
    profissao = data.get('profissao')
    data_nascimento = data.get('data_nascimento')

    # Valida se todos os campos obrigatórios foram enviados no JSON
    if not all([cidade, uf, telefone, palavra_chave, profissao, data_nascimento]):
        return jsonify({"error": "Necessário informar todos os dados requeridos."}), 400
    
    try:
        # Executa as criações e buscas pelos Services
        candidato = CandidatoService.create_candidato(data,user_id)
        usuario = UsuarioService.get_usuario_by_id(user_id)
        
        # Formata o usuário usando seu schema do Pydantic para evitar erro de JSON com o Status
        usuario_formatado = GetUser.model_validate(usuario).model_dump(mode='json')
        
        return jsonify({
            "message": "Candidato criado com sucesso",
            "candidato": {
                "usuario": usuario_formatado,
                "candidato_id": candidato.id,
                "cidade": candidato.cidade,
                "uf": candidato.uf,
                "telefone": candidato.telefone,
                "palavra_chave": candidato.palavra_chave, # Corrigido digitação
                "profissao": candidato.profissao,
                "data_nascimento": str(candidato.data_nascimento) # Convertido para string para o JSON não quebrar
            }
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        db.session.rollback()
        print("ERRO REAL NO SERVIDOR:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    

#Rota para consultar candidato por ID

@candidato_bp.route('/candidato/<int:candidato_id>', methods=['GET'])
#@jwt_required()
def get_candidato_by_id(candidato_id):
    try:
        # Chama o Service para buscar o candidato
        candidato = CandidatoService.get_candidato_by_id(candidato_id)

        # Se o Service retornar None 
        if not candidato:
            return jsonify({"error": "candidato não encontrado."}), 404

        # O Pydantic valida o candidato único e converte o Enum para String com mode='json'
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Candidato encontrado com sucesso",
            "candidato": candidato_formatado
        }), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500


#Listas todos os candidatos do banco
@candidato_bp.route('/candidatos', methods=['GET'])
#@jwt_required()
def get_candidatos():
    try:
        
        candidatos_banco = CandidatoService.get_candidatos()

        if not candidatos_banco:
            return jsonify({"message": "Nenhum candidato cadastrado.", "candidatos": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_candidatos = [GetCandidato.model_validate(u).model_dump(mode='json') for u in candidatos_banco]
        
        # 3. Retorno 
        return jsonify({
            "message": "Candidatos encontrados com sucesso",
            "candidatos": lista_candidatos
        }), 200

    except Exception as e:
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 


#Busca o candidato pelo nome
@candidato_bp.route('/candidato/busca_nome', methods=['GET'])
#@jwt_required()
def get_candidato_nome():

    nome = request.args.get('nome')
 
    if not nome:
        return jsonify({"Informe o nome de um candidato"})



    try:
        
        candidato= CandidatoService.get_candidato(nome)

        if not candidato:
            return jsonify({"message": "Nenhum candidato cadastrado.", "candidato": []}), 200

    
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json')
        
        # Retorno 
        return jsonify({
            "message": "Candidatos encontrados com sucesso",
            "candidatos": candidato_formatado
        }), 200

    except ValueError as e:
            #Candidato não encontrado
            return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

#Busca o candidato que contém palavra chave
@candidato_bp.route('/candidato/palavra_chave', methods=['GET'])
#@jwt_required()
def get_candidato_palavra_chave():

    palavra_chave = request.args.get('palavra')
 
    if not palavra_chave:
        return jsonify({"error": "É necessário informar o parâmetro 'palavra' na URL."}), 400



    try:
        
        candidatos_banco= CandidatoService.get_candidatos_by_palavra_chave(palavra_chave)

        if not candidatos_banco:
            return jsonify({"message": "Nenhum candidato cadastrado.", "candidato": []}), 200

    
        candidatos_formatado = [GetCandidato.model_validate(u).model_dump(mode='json') for u in candidatos_banco]
        # Retorno 
        return jsonify({
            "message": "Candidatos encontrados com sucesso",
            "candidatos": candidatos_formatado
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

