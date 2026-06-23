from models.banco import db
from models.candidato import Candidato
from models.vagas import Vaga, Status
from schemas.vagas_schema import GetVaga
from models.candidatura import Candidatura,Status
from sqlalchemy.orm import joinedload
from datetime import datetime





class CandidaturaService:

    """ Serviço para gerenciar operações de candidaturas. """
    #Criação
    @staticmethod
    def create_candidatura(vaga_id, candidato_id):
        """ Cria uma nova candidatura. """

       # Verifica se candidato já candidatou na vaga

        candidatura_existente = db.session.query(Candidatura).filter_by(vaga_id=vaga_id, candidato_id=candidato_id).first()

        if candidatura_existente:
            # Se encontrou, impede o cadastro disparando a exceção
            raise ValueError("Este candidato já candidatou nesta vaga.")       

       # Verifica se a vaga está aberta 
        vaga = db.session.query(Vaga).filter_by(id=vaga_id).first()
        if not vaga:
            raise ValueError("vaga não encontrada")

        vaga_validada = GetVaga.model_validate(vaga)

        status_vaga = vaga_validada.status
        
        if status_vaga == 'FECHADA':
            raise ValueError('Vaga está inativa.')

        candidatura = Candidatura(
            vaga_id=vaga_id,
            candidato_id=candidato_id,
            
        )
        db.session.add(candidatura)
        db.session.commit()
        return candidatura  

    #Buscas
    @staticmethod
    def get_candidatura_by_id(candidatura_id):
        """ Busca uma vaga pelo ID. """
        candidatura = db.session.get(Candidatura,candidatura_id)
        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        return candidatura
    
    @staticmethod
    def get_candidaturas_by_vaga(vaga_id):
        """ Busca todas as candidaturas. """
        candidaturas = db.session.query(Candidatura).filter_by(vaga_id=vaga_id).all()
        return candidaturas
    
    @staticmethod
    def get_candidaturas_by_candidato(candidato_id):
        """ Busca todas as candidaturas. """
        candidaturas = db.session.query(Candidatura).filter_by(candidato_id=candidato_id).all()
        return candidaturas
    
       
    @staticmethod
    def get_candidaturas_by_status(status:Status):
        """ Busca todas as candidaturas por um status específico."""
        candidaturas = db.session.query(Candidatura).filter_by(status=status).all()
        return candidaturas

    @staticmethod
    def get_candidaturas_by_periodo(data_inicio, data_fim):
        """ Busca todas as candidaturas entre duas datas."""
        candidaturas = db.session.query(Candidatura).filter(Candidatura.data_criacao.between(data_inicio, data_fim)).all()
        return candidaturas
    

   
    
    #Atualização    
    @staticmethod
    def update_candidatura_enviada(candidatura_id):
        """ Atualiza os dados de uma vaga existente. """
        candidatura = db.session.get(Candidatura, candidatura_id)   

        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        if candidatura.status == Status.ENVIADA:
            raise ValueError('candidatura já foi enviada')
        candidatura.status = Status.ENVIADA

        db.session.commit()
        return candidatura
    
    @staticmethod
    def update_candidatura_analise(candidatura_id):
        """ Atualiza os dados de uma vaga existente. """
        candidatura = db.session.get(Candidatura, candidatura_id)   

        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        if candidatura.status == Status.EM_ANALISE:
            raise ValueError('candidatura já foi está em análise')
        candidatura.status = Status.EM_ANALISE

        db.session.commit()
        return candidatura
    
    @staticmethod
    def update_candidatura_entrevista(candidatura_id):
        """ Atualiza os dados de uma vaga existente. """
        candidatura = db.session.get(Candidatura, candidatura_id)   

        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        if candidatura.status == Status.ENTREVISTA:
            raise ValueError('candidatura já foi está na fase de entrevista')
        candidatura.status = Status.ENTREVISTA

        db.session.commit()
        return candidatura
    
    @staticmethod
    def update_candidatura_aprovada(candidatura_id):
        """ Atualiza os dados de uma vaga existente. """
        candidatura = db.session.get(Candidatura, candidatura_id)   

        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        if candidatura.status == Status.APROVADA:
            raise ValueError('candidatura já foi está aprovada')
        candidatura.status = Status.APROVADA

        db.session.commit()
        return candidatura
    
    @staticmethod
    def update_candidatura_reprovaprovada(candidatura_id):
        """ Atualiza os dados de uma vaga existente. """
        candidatura = db.session.get(Candidatura, candidatura_id)   

        if not candidatura:
            raise ValueError("Candidatura não encontrada no banco de dados.")
        if candidatura.status == Status.REPROVADA:
            raise ValueError('candidatura já foi está reprovada')
        candidatura.status = Status.REPROVADA

        db.session.commit()
        return candidatura
    