from config import Config
from sklearn.metrics.pairwise import cosine_similarity
import json
from services.vaga_service import VagaService
from schemas.vagas_schema import GetVaga
from services.candidato_service import CandidatoService
from schemas.candidato_schema import GetCandidato


class Matching:

    @staticmethod
    def __ler_vetor_candidatos(candidato_id):
        "Método estático e privado"
        # 1. Carregar o arquivo JSON
        diretorio = Config.DIRETORIO_CANDIDATO
        nome_arquivo = f"candidato_id_{candidato_id}.json"
        caminho_completo = diretorio / nome_arquivo

        busca_embenddings = [arquivo.name for arquivo in diretorio.iterdir() if arquivo.is_file()]

        if not nome_arquivo in busca_embenddings:
                print(f"Não encontrado embeddings para candidato_id {candidato_id}")
                return None   

        with open(caminho_completo, "r", encoding="utf-8") as arquivo:
            dados_carregados = json.load(arquivo)
            return dados_carregados
        
 
    @staticmethod
    def __ler_vetor_vaga(vaga_id):
            # Carregar o arquivo JSON
            diretorio = Config.DIRETORIO_VAGAS
            nome_arquivo = f"vaga_id_{vaga_id}.json"
            caminho_completo = diretorio / nome_arquivo

            busca_embenddings = [arquivo.name for arquivo in diretorio.iterdir() if arquivo.is_file()]

            if not nome_arquivo in busca_embenddings:
                print(f"Não encontrado embeddings para vaga_id {vaga_id}")
                return None            

            with open(caminho_completo, "r", encoding="utf-8") as arquivo:
                dados_carregados = json.load(arquivo)
                return dados_carregados

    @staticmethod
    def calcular_match(candidato_id,vaga_id):
        "Método publico "
         
        json_candidato = Matching.__ler_vetor_candidatos(candidato_id)
        json_vaga = Matching.__ler_vetor_vaga(vaga_id)

         # Se a vaga não foi encontrada, para a execução do match aqui
        if json_candidato is None or json_vaga is None:
            print("Cancelando cálculo de match por falta de dados.")
            return None

        vetor_candidato = json_candidato['vetor']
        vetor_vaga = json_vaga['vetor']

        # Calcular Similaridade de Cosseno 
        # cosine_similarity retorna um array 2D como [[0.98]], então extraímos o valor float.
        match_score = cosine_similarity(vetor_candidato, vetor_vaga)[0][0]

        return {
            "cosine_similarity": round(float(match_score), 2)
        }
    

    @staticmethod
    def match_candidato_vagas(candidato_id):
        vaga_banco = VagaService.listar_vagas_ativas()
        lista_vagas= [GetVaga.model_validate(v).model_dump(mode='json') for v in vaga_banco]
        lista_vagas_id = [vaga['id'] for vaga in lista_vagas]

        matches_list = []

        for v_id in lista_vagas_id:
            resultado = Matching.calcular_match(candidato_id, v_id)
            
            if resultado and "cosine_similarity" in resultado:
                match_details = {
                    "candidato_id": candidato_id,
                    "vaga_id": v_id,
                    "cosine_similarity": resultado["cosine_similarity"]
                }
                matches_list.append(match_details)
        
        # Ordena a lista de matches pela similaridade de cosseno em ordem decrescente
        matches_list.sort(key=lambda x: x["cosine_similarity"], reverse=True)
        
        return matches_list


    @staticmethod
    def match_vaga_candidatos(vaga_id):
        candidato_orm_objects = CandidatoService.get_candidatos()
        lista_candidatos_formatados = [GetCandidato.model_validate(c).model_dump(mode='json') for c in candidato_orm_objects]
        lista_candidato_id = [candidato['id'] for candidato in lista_candidatos_formatados]

        matches_list = []

        for c_id in lista_candidato_id:
            resultado = Matching.calcular_match(c_id, vaga_id)
            if resultado and "cosine_similarity" in resultado:
                match_details = {
                    "candidato_id": c_id,
                    "vaga_id": vaga_id,
                    "cosine_similarity": resultado["cosine_similarity"]
                }
                matches_list.append(match_details)
        
        # Ordena a lista de matches pela similaridade de cosseno em ordem decrescente
        matches_list.sort(key=lambda x: x["cosine_similarity"], reverse=True)
        
        return matches_list

if __name__ == "__main__":
    from app import app 

    with app.app_context():

        #match = Matching.match_vaga_candidatos(17)
        match = Matching.match_candidato_vagas(3)
        print(match)