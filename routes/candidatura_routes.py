from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.candidatura_service import *
from schemas.candidato_schema import GetCandidato
from schemas.vagas_schema import GetVaga
from schemas.candidatura_schema import GetCandidatura
from datetime import datetime,date


# Carrega classe Blueprint
candidatura_bp = Blueprint('candidatura', __name__)

# Rota para criar candidaturas
@candidatura_bp.route('/candidatura/<int:vaga_id>/<int:candidato_id>', methods=['POST'])
# @jwt_required()
def create_candidatura(vaga_id,candidato_id):
     

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.create_candidatura(vaga_id,candidato_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode="json")
        vaga_dados = candidatura_formatada.get('vaga',{})
  
        
        return jsonify({
        "message": "Candidatura enviada com sucesso",

        "id_candidatura":candidatura_formatada.get('id'),
        "status":candidatura_formatada.get('status'),
        
        "vaga": {
                    "id": vaga_dados.get('id'),
                    "titulo": vaga_dados.get('titulo'),
                    "status": vaga_dados.get('status')

           
        }
    }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        db.session.rollback()
        print("ERRO REAL NO SERVIDOR:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
    
"""
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

        recrutador_dados = vaga_formatada.get('recrutador', {})
        
        return jsonify({
        "message": "Vaga criada com sucesso",
        "vaga": {
            "id": vaga_formatada.get('id'),
            "titulo": vaga_formatada.get('titulo'),
            "descricao": vaga_formatada.get('descricao'),
            "cidade": vaga_formatada.get('cidade'),
            "uf": vaga_formatada.get('uf'),
            "palavra_chave": vaga_formatada.get('palavra_chave'),
            "modalidade": vaga_formatada.get('modalidade'),
            "status": vaga_formatada.get('status'),
            "data_criacao": vaga_formatada.get('data_criacao')
        },
        "recrutador": {
            "empresa": recrutador_dados.get('empresa'),
            "nome": recrutador_dados.get {('usuario',}).get('nome'),
        }
    }), 200

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
            "candidatos": lista_vagas
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


#Busca vagas por status=FECHADA
@vagas_bp.route('/vaga/status/fechada', methods=['GET'])
#@jwt_required()
def get_vagas_fechadas():


    try:
        
        vagas_banco= VagaService.listar_vagas_inativas()

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

#Atualização

#Atualiza Informações da vaga   
@vagas_bp.route('/vaga/<int:vaga_id>', methods=['PUT'])
#@jwt_required()
def update_vaga(vaga_id):
           
    data = request.get_json() or {}
    
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    cidade = data.get('cidade')
    uf = data.get('uf')
    palavra_chave = data.get('palavra_chave')
    modalidade = data.get('modalidade')
    
  
    if not any([titulo,descricao,cidade, uf, palavra_chave,modalidade]):
        return jsonify({"error": "Necessário informar todos os dados requeridos."}), 400
    

    try:
        # Executa as criações e buscas pelos Services
        vaga = VagaService.update_vaga(vaga_id,data)
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode='json')

        recrutador_dados = vaga_formatada.get('recrutador', {})
        
        return jsonify({
        "message": "Vaga atualizada com sucesso",
        "vaga": {
            "id": vaga_formatada.get('id'),
            "titulo": vaga_formatada.get('titulo'),
            "descricao": vaga_formatada.get('descricao'),
            "cidade": vaga_formatada.get('cidade'),
            "uf": vaga_formatada.get('uf'),
            "palavra_chave": vaga_formatada.get('palavra_chave'),
            "modalidade": vaga_formatada.get('modalidade'),
            "status": vaga_formatada.get('status'),
            "data_criacao": vaga_formatada.get('data_criacao')
        },
        "recrutador": {
            "empresa": recrutador_dados.get('empresa'),
            "nome": recrutador_dados.get('usuario', {}).get('nome'),
        }
    }), 200

        
    
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

        recrutador_dados = vaga_formatada.get('recrutador', {})
        
        return jsonify({
        "message": "Vaga atualizada com sucesso",
        "vaga": {
            "id": vaga_formatada.get('id'),
            "titulo": vaga_formatada.get('titulo'),
            "descricao": vaga_formatada.get('descricao'),
            "cidade": vaga_formatada.get('cidade'),
            "uf": vaga_formatada.get('uf'),
            "palavra_chave": vaga_formatada.get('palavra_chave'),
            "modalidade": vaga_formatada.get('modalidade'),
            "status": vaga_formatada.get('status'),
            "data_criacao": vaga_formatada.get('data_criacao')
        },
        "recrutador": {
            "empresa": recrutador_dados.get('empresa'),
            "nome": recrutador_dados.get('usuario', {}).get('nome'),
        }
    }), 200

        
    
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

        recrutador_dados = vaga_formatada.get('recrutador', {})
        
        return jsonify({
        "message": "Vaga atualizada com sucesso",
        "vaga": {
            "id": vaga_formatada.get('id'),
            "titulo": vaga_formatada.get('titulo'),
            "descricao": vaga_formatada.get('descricao'),
            "cidade": vaga_formatada.get('cidade'),
            "uf": vaga_formatada.get('uf'),
            "palavra_chave": vaga_formatada.get('palavra_chave'),
            "modalidade": vaga_formatada.get('modalidade'),
            "status": vaga_formatada.get('status'),
            "data_criacao": vaga_formatada.get('data_criacao')
        },
        "recrutador": {
            "empresa": recrutador_dados.get('empresa'),
            "nome": recrutador_dados.get('usuario', {}).get('nome'),
        }
    }), 200

        
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print = ("ERRO:", str(e)) 
        return jsonify({"error": "Erro interno no servidor."}), 500
       
"""
    
