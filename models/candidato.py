from models.banco import db
from datetime import date



# Classe candidato


class Candidato(db.Model):
    """ 

Essa classe cria a tabela de candidatos no banco de dados. Onde:
id -> recebe um inteiro
id_usuário -> recebe um inteiro sendo o id do 
cidade -> recebe uma string com no máximo 100 caracteres
uf -> recebe uma string com no máximo 2 caracteres
telefone -> recebe uma string com no máximo 11 caracteres
palavra_chave -> recebe uma string com no máximo 100 caracteres
profisso -> recebe uma string com no máximo 100 caracteres
data_nascimento -> recebe uma data

"""

    __tablename__ = 'candidato'
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, unique=True)
    usuario = db.relationship('User',foreign_keys=[user_id], backref=db.backref('candidato', uselist=False)) # usa relationship e backref para facilitar nas querys dispensa fazer consultas complexas (JOINs) manualmente
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    palavra_chave = db.Column(db.String(100), nullable=False)
    profissao = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    @property
    def idade(self):
        """ Calcula a idade do candidato com base na data de nascimento. """
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
