from models.candidatura import Status
from pydantic import BaseModel, Field, Enu
from datetime import date
from typing import Optional

class CreateCandidatura(BaseModel):

    """ 
    
    A candidatura é criada a partir do contexto da aplicação.
    O sistema define automaticamente:
    - candidato
    - vaga
    - data de criação
    - status inicial: ENVIADA

    """

    model_config = {"from_attributes": True}


class GetCandidatura(BaseModel):

    """ Define esquema para consulta de candidaturas. """

    id: int
    id_vaga: int
    id_candidato: int
    nome_candidato: str # Vem do candidato
    titulo_vaga: str # Vem da vaga
    data_criacao: date
    status: Status





    model_config = {"from_attributes": True}


class UpdateCandidatura(BaseModel):

    """ Define esquema para atualização de candidaturas. """

    
    status: Optional[Status] = None

    model_config = {"from_attributes": True}