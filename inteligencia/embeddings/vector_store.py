from config import Config
import json
from pathlib import Path

class Salvar:

    "Classe para salvar os embeddings dos candidatos e vagas em um arquivo json"

    # Salva candidato
    def salvar_vetor_candidato(candidato_id, vetor):
        # 1. Define o caminho do diretório (pasta) onde quer salvar
        diretorio = Config.DIRETORIO_CANDIDATO
        
        # 2. Cria a pasta automaticamente se ela não existir
        diretorio.mkdir(exist_ok=True)
        
        # 3. Junta o caminho da pasta com o nome do arquivo
        nome_arquivo = f"candidato_id_{candidato_id}.json"
        caminho_completo = diretorio / nome_arquivo
        
        vetor_json = {"vetor": vetor}
        
        # 4. Salva usando o caminho completo
        with open(caminho_completo, "w", encoding="utf-8") as a:
            json.dump(vetor_json, a, indent=4)
            
        print(f"Embedding candidato salvo com sucesso em: {caminho_completo}")

  # Salva vaga
    def salvar_vetor_vaga(vaga_id, vetor):
        # 1. Define o caminho do diretório (pasta) onde quer salvar
        diretorio = Config.DIRETORIO_VAGAS
        
        # 2. Cria a pasta automaticamente se ela não existir
        diretorio.mkdir(exist_ok=True)
        
        # 3. Junta o caminho da pasta com o nome do arquivo
        nome_arquivo = f"vaga_id_{vaga_id}.json"
        caminho_completo = diretorio / nome_arquivo
        
        vetor_json = {"vetor": vetor}
        
        # 4. Salva usando o caminho completo
        with open(caminho_completo, "w", encoding="utf-8") as a:
            json.dump(vetor_json, a, indent=4)
            
        print(f"Embedding vaga salvo com sucesso em: {caminho_completo}")



#teste função    
if __name__ == "__main__":
    data = [[1,2,3,4,5,6,7,8,9],
            [1,2,3,4,5,6,7,8,8]]
    Salvar.salvar_vetor_vaga(1,data)

    "Exceutatar com: python -m inteligencia.embeddings.vector_store (executar na raiz do projeto)"