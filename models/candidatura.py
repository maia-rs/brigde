import enum
from models.banco import db
from datetime import datetime



# Classse Status



class Status(enum.Enum):
  
  """ Essa classe usa Enum para definir opções fixas no valor da coluna status da tabela candidaturas """
  ENVIADA = 'ENVIADA'
  EM_ANALISE = 'EM ANALISE'
  ENTREVISTA = 'ENTREVISTA'
  APROVADA = 'APROVADA'
  REPROVADA = 'REPROVADA'  



# Classe candidatura



class Candidatura(db.Model):


    """ 

    Essa classe cria a tabela de candidaturas no banco de dados. Onde:
    id -> recebe um inteiro
    Id_vaga -> recebe um inteiro sendo o id da vaga
    id_candidato -> recebe um inteiro sendo o id do candidato
    data_criacao -> recebe uma data
    status -> recebe umas das opções da classe

    """
    __tablename__ = 'candidaturas'
    id= db.Column(db.Integer, primary_key=True)
    id_vaga = db.Column(db.Integer, db.ForeignKey('vagas.id'), nullable=False)
    vaga = db.relationship('Vaga', backref=db.backref('candidaturas')) # usa relationship e backref para facilitar nas querys dispensa fazer consultas complexas (JOINs) 
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    candidato = db.relationship('Candidato', backref=db.backref('candidaturas')) # usa relationship e backref para facilitar nas querys dispensa fazer consultas complexas (JOINs) manualmente
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.Enum(Status), nullable=False, default=Status.ENVIADA)





    
