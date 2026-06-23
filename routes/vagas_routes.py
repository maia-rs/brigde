from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.vaga_service import *
from schemas.recrutador_schema import GetRecrutador
from schemas.vagas_schema import GetVaga
from schemas.vagas_schema import CreateVaga # Importar o schema de criação
from services.recrutador_service import *
from datetime import datetime,date


# Carrega classe Blueprint
vagas_bp = Blueprint('vagas', __name__)

# Rota para criar vagas
@vagas_bp.route('/vaga/<int:recrutador_id>', methods=['POST'])
# @jwt_required()
def create_vaga(recrutador_id):
    try:
        # 1. Validação de entrada com Pydantic
        vaga_data = CreateVaga.model_validate(request.get_json())
        
        # Executa as criações e buscas pelos Services
        vaga = VagaService.create_vaga(vaga_data.model_dump(), recrutador_id) # Corrigido o nome da função
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        # 2. Resposta simplificada usando o model_dump completo
        response_data = {
            "message": "Vaga criada com sucesso",
            "vaga": vaga_formatada
        }
        return jsonify(response_data), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        db.session.rollback()
        print("ERRO REAL NO SERVIDOR:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    

#Rota para consultar vaga por ID

@vagas_bp.route('/vaga/<int:vaga_id>', methods=['GET'])
#@jwt_required()
def get_vaga_by_id(vaga_id):
    try:
        # Chama o Service para buscar a vaga
        vaga = VagaService.get_vaga_by_id(vaga_id)

        # Se o Service retornar None 
        if not vaga:
            return jsonify({"error": "vaga não encontrada."}), 404

        # O Pydantic valida a vaga única e converte o Enum para String com mode='json'
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        # Resposta simplificada usando o model_dump completo
        response_data = {
            "message": "Vaga encontrada com sucesso", # Mensagem mais apropriada
            "vaga": vaga_formatada
        }
        return jsonify(response_data), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

#Listas todos as vagas do banco
@vagas_bp.route('/vaga', methods=['GET'])
#@jwt_required()
def get_vagas():
    try:
        
        vagas_banco = VagaService.get_vagas()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vagas": []}), 200

        # Pydantic varre a lista do Service e converte o status automaticamente
        lista_vagas = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        
        # 3. Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": lista_vagas
        }), 200
    
    except ValueError as e:
            #Vagas não encontradas
            return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 



#Busca a vaga por parte do título
@vagas_bp.route('/vaga/titulo_parcial', methods=['GET'])
#@jwt_required()
def get_vaga_titulo():

    titulo_parcial = request.args.get('titulo_parcial')
 
    if not titulo_parcial:
        return jsonify({"error": "É necessário informar o parâmetro 'titulo_parcial' na URL."}), 400



    try:
        
        vagas_banco= VagaService.get_vagas_by_parcial_titulo(titulo_parcial)

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Vaga não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 



#Busca a vaga que contém palavra chave
@vagas_bp.route('/vaga/palavra_chave', methods=['GET'])
#@jwt_required()
def get_vaga_palavra_chave():

    palavra_chave = request.args.get('palavra_chave')
 
    if not palavra_chave:
        return jsonify({"error": "É necessário informar o parâmetro 'palavra_chave' na URL."}), 400



    try:
        
        vagas_banco= VagaService.get_vaga_by_palavra_chave(palavra_chave)

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Vaga não encontrada
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500




#Rota para consultar vaga por recrutador

@vagas_bp.route('/vaga/recrutador/<int:recrutador_id>', methods=['GET'])
#@jwt_required()
def get_vaga_by_recrutador(recrutador_id):
    try:
        # Chama o Service para buscar a vaga
        vagas_banco = VagaService.get_vagas_by_recrutador(recrutador_id)

        # Se o Service retornar None 
        if not vagas_banco:
            return jsonify({"error": "vaga não encontrada."}), 404

        # O Pydantic valida a vaga única e converte o Enum para String com mode='json'
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]

        
        return jsonify({
        "message": "Vagas encontradas com sucesso",
        "vagas": vagas_formatada
        
    }), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500


#Busca vagas por cidade
@vagas_bp.route('/vaga/cidade', methods=['GET'])
#@jwt_required()
def get_vagas_cidade():

    cidade = request.args.get('cidade')
 
    if not cidade:
        return jsonify({"error": "É necessário informar o parâmetro 'cidade' na URL."}), 400



    try:
        
        vagas_banco= VagaService.get_vagas_by_cidade(cidade)

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    


#Busca vagas por uf
@vagas_bp.route('/vaga/uf', methods=['GET'])
#@jwt_required()
def get_vagas_uf():

    uf = request.args.get('uf')
 
    if not uf:
        return jsonify({"error": "É necessário informar o parâmetro 'uf' na URL."}), 400



    try:
        
        vagas_banco= VagaService.get_vagas_by_uf(uf)

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "vagas encontrados com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

 
    

# Busca o vaga por periodo de criação

@vagas_bp.route('/vaga/periodo', methods=['GET'])
# @jwt_required()
def get_vaga_periodo():

    data_inicio_texto = request.args.get('data_inicio')
    data_fim_texto = request.args.get('data_fim')

    if not data_inicio_texto and data_fim_texto:
        return jsonify({"error": "É necessário informar o parâmetro 'data_inicio' e 'data_fim' na URL."}), 400

    try:
        # Converte o texto recebido em um objeto date do Python
        data_inicio_convertida = datetime.strptime(data_inicio_texto, "%Y-%m-%d").date()
        data_fim_convertida = datetime.strptime(data_fim_texto, "%Y-%m-%d").date()


        vagas_banco = VagaService.get_vagas_by_periodo(data_inicio_convertida,data_fim_convertida)

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga encontrada para esta periodo.", "vagas": []}), 200

        # 4. Formata a lista usando o Pydantic
        vagas_formatada = [GetVaga.model_validate(v).model_dump(mode='json') for v in vagas_banco]

        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200

    except ValueError as e:
    # Trata formato incorreto de data enviado na URL 
        if "time data" in str(e):
            return jsonify({"error": "Formato de data inválido na URL. Use o padrão AAAA-MM-DD."}), 400
        return jsonify({"message": str(e), "candidatos": []}), 404

    except Exception as e:
        db.session.rollback()
        print("ERRO INTERNO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}),500
    

#Busca vagas por modalidade=presencial
@vagas_bp.route('/vaga/modalidade/presencial', methods=['GET'])
#@jwt_required()
def get_vagas_presencial():


    try:
        
        vagas_banco= VagaService.listar_vagas_presencial()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"candidatos":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    



#Busca vagas por modalidade=hibrida
@vagas_bp.route('/vaga/modalidade/hibrida', methods=['GET'])
#@jwt_required()
def get_vagas_hibrida():


    try:
        
        vagas_banco= VagaService.listar_vagas_hibrido()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500




#Busca vagas por modalidade=home_office
@vagas_bp.route('/vaga/modalidade/homeoffice', methods=['GET'])
#@jwt_required()
def get_vagas_homeoffice():


    try:
        
        vagas_banco= VagaService.listar_vagas_home_office()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga cadastrada.", "vaga": []}), 200

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500




#Busca vagas por status=Aberta
@vagas_bp.route('/vaga/status/aberta', methods=['GET'])
#@jwt_required()
def get_vagas_abertas():


    try:
        
        vagas_banco= VagaService.listar_vagas_ativas()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga aberta encontrada.", "vagas": []}), 200 # Mensagem mais específica

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500


#Busca vagas por status=FECHADA
@vagas_bp.route('/vaga/status/fechada', methods=['GET'])
#@jwt_required()
def get_vagas_fechadas():


    try:
        
        vagas_banco= VagaService.listar_vagas_inativas()

        if not vagas_banco:
            return jsonify({"message": "Nenhuma vaga fechada encontrada.", "vagas": []}), 200 # Mensagem mais específica

    
        vagas_formatada = [GetVaga.model_validate(u).model_dump(mode='json') for u in vagas_banco]
        # Retorno 
        return jsonify({
            "message": "Vagas encontradas com sucesso",
            "vagas": vagas_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500

#Atualização

#Atualiza Informações da vaga   
@vagas_bp.route('/vaga/<int:vaga_id>', methods=['PUT'])
#@jwt_required()
def update_vaga(vaga_id):
    try:
        # 1. Validação de entrada com Pydantic
        vaga_data = UpdateVaga.model_validate(request.get_json())
        
        # Executa as criações e buscas pelos Services
        vaga = VagaService.update_vaga(vaga_id, vaga_data.model_dump(exclude_unset=True)) # Passa o dicionário validado
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        # 2. Resposta simplificada usando o model_dump completo
        response_data = {
            "message": "Vaga atualizada com sucesso",
            "vaga": vaga_formatada
        }
        return jsonify(response_data), 200

        
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    

    #Desativa uma vaga


#Atualiza Informações da vaga   
@vagas_bp.route('/vaga/desativar/<int:vaga_id>', methods=['PUT'])
#@jwt_required()
def desativa_vaga(vaga_id):  

    try:
        # Executa as criações e buscas pelos Services
        vaga = VagaService.desativar_vaga(vaga_id)
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        response_data = {
            "message": "Vaga desativada com sucesso", # Mensagem mais específica
            "vaga": vaga_formatada
        }
        return jsonify(response_data), 200

        
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    

 #Atualiza Informações da vaga   
@vagas_bp.route('/vaga/ativar/<int:vaga_id>', methods=['PUT'])
#@jwt_required()
def ativa_vaga(vaga_id):  

    try:
        # Executa as criações e buscas pelos Services
        vaga = VagaService.ativar_vaga(vaga_id)
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        response_data = {
            "message": "Vaga ativada com sucesso", # Mensagem mais específica
            "vaga": vaga_formatada
        }
        return jsonify(response_data), 200

        
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
       

    
