import enum
from models.banco import db
from datetime import datetime



# Classe enum para opções de modalidade


class Modalidade(enum.Enum):

    """ Essa classe usa Enum para definir opções fixas no valor da coluna modalidade da tabela vagas"""

    PRESENCIAL = 'PRESENCIAL'
    HIBRIDO = 'HIBRIDO'
    HOME_OFFICE = 'HOME OFFICE'

# Classse Status


class Status(enum.Enum):

    """ Essa classe usa Enum para definir opções fixas no valor da coluna status da tabela vagas """

    ATIVO = 'ABERTA'
    INATIVO = 'FECHADA'



# Classe Vaga

class Vaga(db.Model):

    """ 

    Essa classe cria a tabela de vagas no banco de dados. Onde:
    id -> recebe um inteiro
    id_usuário -> recebe um inteiro sendo o id do 
    cidade -> recebe uma string com no máximo 100 caracteres
    uf -> recebe uma string com no máximo 2 
    palavra_chave -> recebe uma string com no máximo 100 caracteres
    modalidade -> recebe umas das opções da classe Modalidade
    data_criacao -> recebe uma data
    status -> recebe umas das opções da classe 
        
    """
    __tablename__ = 'vagas'
    id= db.Column(db.Integer, primary_key=True)
    recrutador_id = db.Column(db.Integer, db.ForeignKey('recrutador.id'), nullable=False)
    recrutador = db.relationship('Recrutador', backref=db.backref('vagas')) # usa relationship e backref para facilitar nas querys dispensa fazer consultas complexas (JOINs) manualmente
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)   
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    palavra_chave = db.Column(db.String(100), nullable=False)
    modalidade = db.Column(db.Enum(Modalidade), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.ATIVO)
    
    
