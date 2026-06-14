from models.banco import db



# Classe recrutador




class Recrutador(db.Model):

    """ 

Essa classe cria a tabela de recrutador no banco de dados. Onde:
id -> recebe um inteiro
id_usuário -> recebe um inteiro sendo o id do 
empresa -> recebe uma string com no máximo 100 caracteres


"""
    __tablename__ = 'recrutador'
    id= db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, unique=True)
    usuario = db.relationship('User', backref=db.backref('recrutador', uselist=False)) # usa relationship e backref para facilitar nas querys dispensa fazer consultas complexas (JOINs) manualmente
    empresa = db.Column(db.String(100), nullable=False)
    
