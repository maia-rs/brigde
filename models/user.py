import enum
from models.banco import db

# Classe enum para opções de perfil



class PerfilUser(enum.Enum):

    """ Essa classe usa Enum para definir opções fixas no valor da coluna perfil da tabela user"""
    
    CANDIDATO = 'CANDIDATO'
    RECRUTADOR = 'RECRUTADOR'
    ADMINISTRADOR = 'ADMINISTRADOR'


# Classse Status



class Status(enum.Enum):

    """ Essa classe usa Enum para definir opções fixas no valor da coluna status da tabela user """

    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'



# Classe usuário 



class User(db.Model):


    """ 

    Essa classe cria a tabela de usuários no banco de dados. Onde:
    id -> recebe um inteiro
    nome -> recebe uma string com no máximo 100 caracteres
    email -> recebe uma string com no máximo 100 caracteres
    perfil -> recebe umas das opções da classe PerfilUser
    senha -> recebe uma string com no máximo 100 caracteres
    status -> recebe umas das opções da classe 

    """
    __tablename__ = 'usuario'
    id= db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # perfil = db.Column(db.Enum(PerfilUser), nullable=False, default=PerfilUser.CANDIDATO) 
    senha = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.ATIVO)

 