import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DATABASE_URI = os.getenv("DATABASE_URI")
    
    # Lendo o texto do .env e transformando em objeto Path
    # O segundo argumento é o valor padrão caso a linha suma do .env por erro
    DIRETORIO_CANDIDATO = Path(os.getenv("DIRETORIO_CANDIDATO", "vetores_candidatos"))
    DIRETORIO_VAGAS = Path(os.getenv("DIRETORIO_VAGAS", "vetores_vagas"))
