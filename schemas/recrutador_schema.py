from pydantic import BaseModel, Field
from typing import Optional

class CreateRecrutador(BaseModel):

    """ Define a criação de recrutador usando Pydantic. """

    empresa: str = Field(..., min_length=3, max_length=100)

    model_config = {"from_attributes": True}


class GetRecrutador(BaseModel):

    """ Define esquema para consulta de recrutadores. """

    id: int
    id_usuario: int
    nome: str
    email: str
    empresa: str

    model_config = {"from_attributes": True}


class UpdateRecrutador(BaseModel):

    """ Define esquema para atualização de recrutadores. """

    empresa: Optional[str] = Field(None, min_length=3, max_length=100)

    model_config = {"from_attributes": True}
