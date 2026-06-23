from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.banco import db
from services.candidatura_service import *
from schemas.candidato_schema import GetCandidato
from schemas.vagas_schema import GetVaga
from schemas.candidatura_schema import GetCandidatura
from datetime import datetime,date

# Importar o schema de criação, se houver (CreateCandidatura é vazio, mas é bom ter o import)
# Carrega classe Blueprint
candidatura_bp = Blueprint('candidatura', __name__)

# Rota para criar candidaturas
@candidatura_bp.route('/candidatura/<int:vaga_id>/<int:candidato_id>', methods=['POST'])
# @jwt_required()
def create_candidatura(vaga_id,candidato_id):
     

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.create_candidatura(vaga_id,candidato_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')
        
        # Resposta simplificada usando o model_dump completo
        return jsonify({"message": "Candidatura enviada com sucesso", "candidatura": candidatura_formatada}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        db.session.rollback()
        print("ERRO REAL NO SERVIDOR:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500
    

#Rota para consultar candidatura por ID

@candidatura_bp.route('/candidatura/<int:candidatura_id>', methods=['GET'])
#@jwt_required() # Manter comentado se não for para usar JWT
def get_candidatura_by_id_route(candidatura_id): # Renomeado para refletir a busca por candidatura_id
    try:
        # Chama o Service para buscar a candidatura
        candidatura = CandidaturaService.get_candidatura_by_id(candidatura_id) # O service já busca por candidatura_id

        # Se o Service retornar None 
        if not candidatura:
            return jsonify({"error": "candidatura não encontrada."}), 404

        # O Pydantic valida a candidatura única e converte o Enum para String com mode='json'
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')

       
        
        # Resposta simplificada
        return jsonify({"message": "Candidatura encontrada com sucesso", "candidatura": candidatura_formatada}), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 




#Rota para consultar candidatura por candidato

@candidatura_bp.route('/candidatura/candidato/<int:candidato_id>', methods=['GET'])
#@jwt_required()
def get_candidatura_by_candidato_id(candidato_id):
    try:
        # Chama o Service para buscar a candidatura
        candidaturas_banco = CandidaturaService.get_candidaturas_by_candidato(candidato_id)

        # Se o Service retornar None 
        if not candidaturas_banco:
            return jsonify({"error": "candidatura não encontrada."}), 404

        # O Pydantic valida a vaga única e converte o Enum para String com mode='json'
        candidatura_formatada = [GetCandidatura.model_validate(c).model_dump(mode='json') for c in candidaturas_banco]

       
        
        # Resposta simplificada
        return jsonify({"message": "Candidatura encontrada com sucesso", "candidaturas": candidatura_formatada}), 200

    except ValueError as e:
        # Captura erros 
        return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado no servidor
        db.session.rollback()
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500
    



#Rota para consultar candidatura por periodo

@candidatura_bp.route('/candidatura/periodo', methods=['GET'])

#@jwt_required()
def get_candidatura_by_periodo():
        
        data_inicio_texto = request.args.get('data_inicio')
        data_fim_texto = request.args.get('data_fim')

        if not data_inicio_texto or not data_fim_texto: # Condição corrigida
            return jsonify({"error": "É necessário informar os parâmetros 'data_inicio' e 'data_fim' na URL."}), 400
        

        try:
            # Converte o texto recebido em um objeto date do Python
            data_inicio_convertida = datetime.strptime(data_inicio_texto, "%Y-%m-%d").date()
            data_fim_convertida = datetime.strptime(data_fim_texto, "%Y-%m-%d").date()


            candidaturas_banco = CandidaturaService.get_candidaturas_by_periodo(data_inicio_convertida,data_fim_convertida)

            if not candidaturas_banco:
                return jsonify({"message": "Nenhuma candidatura encontrada para este período.", "candidaturas": []}), 200

            # 4. Formata a lista usando o Pydantic
            candidaturas_formatada = [GetCandidatura.model_validate(c).model_dump(mode='json') for c in candidaturas_banco]

            return jsonify({
                "message": "Vagas encontradas com sucesso",
                "vagas": candidaturas_formatada
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


#Busca Candidatura por Status
@candidatura_bp.route('/candidatura/status', methods=['GET'])
#@jwt_required()
def get_candidatura_status():

    status = request.args.get('status')

    if not status:
        return jsonify({'erro':'Necesário informar um status para busca',
                        'status':'ENVIADA, EM_ANALISE, ENTREVISTA , APROVADA, REPROVADA '}),400


    try:
        
        candidaturas_banco= CandidaturaService.get_candidaturas_by_status(status)

        if not candidaturas_banco:
            return jsonify({"message": "Nenhuma candidatura encontrada para este status.", "candidaturas": []}), 200

    
        candidatura_formatada = [GetCandidatura.model_validate(u).model_dump(mode='json') for u in candidaturas_banco]
        # Retorno 
        return jsonify({
            "message": "Candidaturas encontradas com sucesso",
            "candidaturas": candidatura_formatada
        }), 200
    
    except ValueError as e:
        #Candidato não encontrado
        return jsonify({"mensagem":str(e),"vagas":[]})


    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500

#Atualização

 #Atualiza Informações da candidatura   
@candidatura_bp.route('/candidatura/enviada/<int:candidatura_id>', methods=['PUT'])
#@jwt_required()
def envia_candidatura(candidatura_id):  

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.update_candidatura_enviada(candidatura_id) 
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')


        
        return jsonify({
        "message": "candidatura enviada com sucesso",
        "Dados": candidatura_formatada
        
    }), 200

        
    
    except ValueError as e:
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback()
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500


 #Atualiza Informações da candidatura
@candidatura_bp.route('/candidatura/em_analise/<int:candidatura_id>', methods=['PUT'])
#@jwt_required()
def em_analise_candidatura(candidatura_id):

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.update_candidatura_analise(candidatura_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')



        return jsonify({
        "message": "Candidatura em análise com sucesso",
        "Dados": candidatura_formatada

    }), 200



    except ValueError as e:
            return jsonify({"error": str(e)}), 422

    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback() # Corrigido o print
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500


 #Atualiza Informações da candidatura
@candidatura_bp.route('/candidatura/entrevista/<int:candidatura_id>', methods=['PUT'])
#@jwt_required()
def entrevista_candidatura(candidatura_id):

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.update_candidatura_entrevista(candidatura_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')



        return jsonify({
        "message": "Candidatura em entrevista com sucesso",
        "Dados": candidatura_formatada

    }), 200



    except ValueError as e:
            return jsonify({"error": str(e)}), 422

    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback() # Corrigido o print
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500


 #Atualiza Informações da candidatura
@candidatura_bp.route('/candidatura/aprovada/<int:candidatura_id>', methods=['PUT'])
#@jwt_required()
def aprovada_candidatura(candidatura_id):

    try:
        # Executa as criações e buscas pelos Services
        candidatura = CandidaturaService.update_candidatura_aprovada(candidatura_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')



        return jsonify({
        "message": "Candidatura aprovada com sucesso",
        "Dados": candidatura_formatada

    }), 200



    except ValueError as e:
            return jsonify({"error": str(e)}), 422

    except Exception as e:
        # Erro inesperado do banco ou servidor
        db.session.rollback() # Corrigido o print
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500


 #Atualiza Informações da candidatura
@candidatura_bp.route('/candidatura/reprovada/<int:candidatura_id>', methods=['PUT'])
#@jwt_required()
def reprovada_candidatura(candidatura_id):

    try:
        candidatura = CandidaturaService.update_candidatura_reprovaprovada(candidatura_id)
        candidatura_formatada = GetCandidatura.model_validate(candidatura).model_dump(mode='json')
        return jsonify({"message": "Candidatura reprovada com sucesso", "Dados": candidatura_formatada}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        db.session.rollback()
        print("ERRO:", str(e))
        return jsonify({"error": "Erro interno no servidor."}), 500
       
