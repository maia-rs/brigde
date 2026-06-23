from models.user import Status
from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

# Schema usuário

class CreateUser(BaseModel):

    """ Define a criação de usuário usando Pydantic. """


    nome: str = Field(...,min_length=3, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    senha: str = Field(..., min_length=6, max_length=100)

    model_config = {"from_attributes": True} 

class GetUser(BaseModel):

    """ Define esquema para consulta de usuários. """

    id: int
    nome: str
    email: EmailStr
    status: Status



    model_config = {"from_attributes": True}

class UpdateUser(BaseModel):

    """ Define esquema para atualização de usuários. """

    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[str] = Field(None, min_length=3, max_length=100)
    senha: Optional[str] = Field(None, min_length=6, max_length=100)
    status: Optional[Status] = None


    model_config = {"from_attributes": True}


# Schema Login

class Login(BaseModel):

    """ Define esquema para login de usuários. Sendo possível fazer login com e-mail. """

    #nome: Optional[str] = None
    email: EmailStr = Field(..., description="Endereço de e-mail do usuário")
    senha: str = Field(..., min_length=6, description="Senha do usuário")


    model_config = {"from_attributes": True}
