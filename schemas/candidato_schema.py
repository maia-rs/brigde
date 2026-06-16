from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Schema usuário

class CreateCandidato(BaseModel):

    """ Define a criação de usuário usando Pydantic. """

    cidade: str = Field(..., min_length=3, max_length=100)
    uf: str = Field(..., min_length=2, max_length=2)
    telefone: str = Field(..., min_length=11, max_length=11)
    palavra_chave: str = Field(..., min_length=3, max_length=100)
    profissao: str = Field(..., min_length=3, max_length=100)
    data_nascimento:date


    model_config = {"from_attributes": True}


class GetCandidato(BaseModel):

    """ Define esquema para consulta de candidatos. """

    id: int
    id_usuario: int
    nome: str 
    email: str
    cidade: str
    uf: str
    telefone: str
    palavra_chave: str
    profissao: str
    data_nascimento: date
    idade: int



    model_config = {"from_attributes": True}

class UpdateCandidato(BaseModel):

    """ Define esquema para atualização de candidatos. """

    cidade: Optional[str] = Field(None, min_length=3, max_length=100)
    uf: Optional[str] = Field(None, min_length=2, max_length=2)
    telefone: Optional[str] = Field(None, min_length=11, max_length=11)
    palavra_chave: Optional[str] = Field(None, min_length=3, max_length=100)
    profissao: Optional[str] = Field(None, min_length=3, max_length=100)
    data_nascimento: Optional[date] = None

    model_config = {"from_attributes": True}
