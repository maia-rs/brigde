from models.vagas import Status, Modalidade
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class CreateVaga(BaseModel):
    """ Define a criação de vagas usando Pydantic. """

    titulo: str = Field(..., min_length=3, max_length=100)
    descricao: str = Field(..., min_length=3, max_length=1000)
    cidade: str = Field(..., min_length=3, max_length=100)
    uf: str = Field(..., min_length=2, max_length=2)
    palavra_chave: str = Field(..., min_length=3, max_length=100)
    modalidade: Modalidade
    #data_criacao: date

    model_config = {"from_attributes": True}


class GetVaga(BaseModel):
    """ Define esquema para consulta de vagas. """

    id: int
    id_recrutador: int
    nome_recrutador: str # Vem do recrutador
    empresa: str # Vem do recrutador
    titulo: str
    descricao: str
    cidade: str
    uf: str
    palavra_chave: str
    modalidade: Modalidade
    #data_criacao: date
    status: Status


    model_config = {"from_attributes": True}


class UpdateVaga(BaseModel):
    """ Define esquema para atualização de vagas. """

    titulo: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, min_length=3, max_length=1000)
    cidade: Optional[str] = Field(None, min_length=3, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    palavra_chave: Optional[str] = Field(None, min_length=3, max_length=100)
    modalidade: Optional[Modalidade] = None
    status: Optional[Status] = None
    #data_criacao: Optional[date] = None


    model_config = {"from_attributes": True}



