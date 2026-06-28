import ollama
# Removed logging, numpy, Config import, @staticmethod, try-except, and type hints
# Reverted to original class structure and method signature


class Embedding:
    """ Classe para gerar embeddings de candidato e vaga """

    def gerar_embeddings(data):
        vetor = ollama.embed(
            model="embeddinggemma", #Modelo ollama local para gerar embeddings (opção = nomic-embed-text, mxbai-embed-large,embeddinggemma,qwen3-embedding:4b)
            input=data
        )
        return vetor["embeddings"]

# teste função
if __name__ == "__main__":
    from app import app #importado para teste da função
    from services.candidato_service import CandidatoService # importado para teste da função
    from schemas.candidato_schema import GetCandidato # importado para teste da função
    with app.app_context():
        candidato = CandidatoService.get_candidato_by_id(candidato_id=1)
        candidato_formatado = GetCandidato.model_validate(candidato).model_dump(mode='json') 
        data = f'cidade: {candidato_formatado['cidade']},\
                 uf{candidato_formatado['uf']},\
                 palavra_chave{candidato_formatado['palavra_chave']},\
                 profissao{candidato_formatado['profissao']}'
        vetor = Embedding.gerar_embeddings(data)
        print(vetor)
    """Exceutatar com: python -m inteligencia.embeddings.embeddings (executar na raiz do projeto)"""