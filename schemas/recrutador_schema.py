from pydantic import BaseModel, Field
from typing import Optional
from schemas.user_schema import GetUser

class CreateRecrutador(BaseModel):

    """ Define a criação de recrutador usando Pydantic. """

    empresa: str = Field(..., min_length=3, max_length=100)

    model_config = {"from_attributes": True}


class GetRecrutador(BaseModel):

    """ Define esquema para consulta de recrutadores. """

    id: int
    user_id: int
    empresa: str

    usuario:GetUser

    model_config = {"from_attributes": True}


class UpdateRecrutador(BaseModel):

    """ Define esquema para atualização de recrutadores. """

    empresa: Optional[str] = Field(None, min_length=3, max_length=100)

    model_config = {"from_attributes": True}
