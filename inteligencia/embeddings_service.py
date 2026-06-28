from inteligencia.embeddings.embeddings import Embedding
from inteligencia.embeddings.vector_store import Salvar
from schemas.candidato_schema import GetCandidato
from schemas.vagas_schema import GetVaga

class Embenddings:

    def criar_embeddings_candidato(candidato_id):
        from services.candidato_service import CandidatoService
        candidato = CandidatoService.get_candidato_by_id(candidato_id)
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json')
        # transforma o json do modelo no formato(str) suportado pelo modelo ollama 
        data = f'cidade: {candidato_formatado['cidade']},\
                 uf{candidato_formatado['uf']},\
                 palavra_chave{candidato_formatado['palavra_chave']},\
                 profissao{candidato_formatado['profissao']}'

        embeddings = Embedding.gerar_embeddings(data)
        salvar = Salvar.salvar_vetor_candidato(candidato_id,embeddings)

        return salvar   

    def criar_embeddings_vagas(vaga_id):
        from services.vaga_service import VagaService
        vaga = VagaService.get_vaga_by_id(vaga_id)
        vaga_formatada = GetVaga.model_validate(vaga).model_dump(mode="json")
        data = f"titulo: {vaga_formatada['titulo']},\
                 descricao: {vaga_formatada['descricao']},\
                 palavra_chave: {vaga_formatada['palavra_chave']},\
                 cidade: {vaga_formatada['cidade']},\
                 uf: {vaga_formatada['uf']},\
                 modalidade: {vaga_formatada['modalidade']}"
        embeddings = Embedding.gerar_embeddings(data)
        salvar = Salvar.salvar_vetor_vaga(vaga_id,embeddings)

        return salvar

if __name__ == "__main__":
    from app import app 
    with app.app_context():
        Embenddings.criar_embeddings_candidato(candidato_id=1)
        Embenddings.criar_embeddings_vagas(vaga_id=17)
        """Exceutatar com:  python-m inteligencia.embeddings_service (executar na raiz do projeto)"""   