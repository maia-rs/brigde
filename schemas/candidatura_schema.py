from models.candidatura import Status
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from schemas.candidato_schema import GetCandidato
from schemas.vagas_schema import GetVaga

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
    vaga_id: int
    candidato_id: int
    #nome_candidato: str # Vem do candidato
    #titulo_vaga: str # Vem da vaga
    data_criacao: datetime
    status: Status

    candidato:GetCandidato
    vaga:GetVaga



    model_config = {"from_attributes": True}


class UpdateCandidatura(BaseModel):

    """ Define esquema para atualização de candidaturas. """

    
    status: Optional[Status] = None

    model_config = {"from_attributes": True}