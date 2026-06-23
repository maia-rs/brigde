from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.candidato_service import *
from schemas.user_schema import GetUser
from schemas.candidato_schema import GetCandidato
from schemas.candidato_schema import CreateCandidato, UpdateCandidato # Importar schemas de criação e atualização
from services.user_service import *
from datetime import datetime



# Carrega classe Blueprint
candidato_bp = Blueprint('candidato', __name__)

# Rota para criar candidato
@candidato_bp.route('/candidato/<int:user_id>', methods=['POST'])
# @jwt_required()
def create_candidato_perfil(user_id):
    try:
        # 1. Validação de entrada com Pydantic
        candidato_data = CreateCandidato.model_validate(request.get_json())
        
        # Executa as criações e buscas pelos Services
        candidato = CandidatoService.create_candidato(candidato_data.model_dump(), user_id)
        
        # Formata o candidato usando seu schema do Pydantic
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json')
        
        # Resposta simplificada
        return jsonify({"message": "Candidato criado com sucesso", "candidato": candidato_formatado}), 201

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
    
    except ValueError as e:
            #Candidato não encontrado
            return jsonify({"mensagem":str(e),"candidatos":[]})


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
            "candidato": candidato_formatado # Chave corrigida para um único candidato
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

#Busca o candidato por cidade
@candidato_bp.route('/candidato/cidade', methods=['GET'])
#@jwt_required()
def get_candidato_cidade():

    cidade = request.args.get('cidade')
 
    if not cidade:
        return jsonify({"error": "É necessário informar o parâmetro 'cidade' na URL."}), 400



    try:
        
        candidatos_banco= CandidatoService.get_candidatos_by_cidade(cidade)

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


#Busca o candidato por uf
@candidato_bp.route('/candidato/uf', methods=['GET'])
#@jwt_required()
def get_candidato_uf():

    uf = request.args.get('uf')
 
    if not uf:
        return jsonify({"error": "É necessário informar o parâmetro 'uf' na URL."}), 400



    try:
        
        candidatos_banco= CandidatoService.get_candidatos_by_uf(uf)

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
    
#Busca o candidato por profissão
@candidato_bp.route('/candidato/profissao', methods=['GET'])
#@jwt_required()
def get_candidato_profissao():

    profissao = request.args.get('profissao')
 
    if not profissao:
        return jsonify({"error": "É necessário informar o parâmetro 'profissao' na URL."}), 400

    try:
        
        candidatos_banco= CandidatoService.get_candidatos_by_profissao(profissao)

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

#Busca o candidato por idade
@candidato_bp.route('/candidato/idade/<int:idade>', methods=['GET'])
#@jwt_required()
def get_candidato_idade(idade):

    #idade = request.args.get('idade')
 
    if not idade:
        return jsonify({"error": "É necessário informar o parâmetro 'idade' na URL."}), 400

    try:
        
        candidatos_banco= CandidatoService.get_candidatos_by_idade(idade)

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
    
    

# Busca o candidato por data de nascimento

@candidato_bp.route('/candidato/data_nascimento', methods=['GET'])
# @jwt_required()
def get_candidato_data_nascimento():
    # 1. Captura a string da URL: /candidato/data_nascimento?data=2000-05-15
    data_texto = request.args.get('data')

    if not data_texto:
        return jsonify({"error": "É necessário informar o parâmetro 'data' na URL."}), 400

    try:
        # 2. Converte o texto recebido em um objeto date do Python
        data_convertida = datetime.strptime(data_texto, "%Y-%m-%d").date()
        
        # 3. Chama o Service passando a data já convertida
        candidatos_banco = CandidatoService.get_candidatos_by_data_nascimento(data_convertida)

        if not candidatos_banco:
            return jsonify({"message": "Nenhum candidato encontrado para esta data.", "candidatos": []}), 200

        # 4. Formata a lista usando o Pydantic
        candidatos_formatado = [GetCandidato.model_validate(c).model_dump(mode='json') for c in candidatos_banco]
        
        return jsonify({
            "message": "Candidatos encontrados com sucesso",
            "candidatos": candidatos_formatado
        }), 200

    except ValueError as e:
        # Trata formato incorreto de data enviado na URL 
        if "time data" in str(e):
            return jsonify({"error": "Formato de data inválido na URL. Use o padrão AAAA-MM-DD."}), 400
        return jsonify({"message": str(e), "candidatos": []}), 404

    except Exception as e:
        db.session.rollback()
        print("ERRO INTERNO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

#Atualização

#Atualiza Informações do usuário   
@candidato_bp.route('/candidato/<int:candidato_id>', methods=['PUT'])
#@jwt_required()
def update_candidato(candidato_id):
    try:
        # 1. Validação de entrada com Pydantic
        candidato_data = UpdateCandidato.model_validate(request.get_json())
        
        # Chama o Service para atualizar o candidato
        candidato = CandidatoService.update_candidato(candidato_id, candidato_data.model_dump(exclude_unset=True))

        # Se o Service retornar None 
        if not candidato:
            return jsonify({"error": "Candidato não encontrado."}), 404
        
        # O Pydantic valida o usuário único e converte o Enum para String com mode='json'
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json')

        # Retorno 
        return jsonify({
            "message": "Candidato atualizado com sucesso",
            "candidato": candidato_formatado
        }), 200
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print("ERRO:", str(e)) # Corrigido o print
        return jsonify({"error": "Erro interno no servidor.", "details": str(e)}), 500
