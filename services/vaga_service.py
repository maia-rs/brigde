from models.banco import db
from models.recrutador import Recrutador
from models.vagas import Vaga, Status,Modalidade
from sqlalchemy.orm import joinedload


class VagaService:

    """ Serviço para gerenciar operações de vagas. """
    #Criação
    @staticmethod
    def creat_vaga(data, recrutador_id):
        """ Cria uma nova vaga. """
        vaga = Vaga(
            recrutador_id=recrutador_id,
            titulo=data['titulo'],
            descricao=data['descricao'],
            cidade=data['cidade'],
            uf=data['uf'],
            palavra_chave=data['palavra_chave'],
            modalidade=data['modalidade'],
            
        )
        db.session.add(vaga)
        db.session.commit()
        return vaga  

    #Buscas

    @staticmethod
    def get_vaga_by_id(vaga_id):
        """ Busca uma vaga pelo ID. """
        vaga = db.session.get(Vaga,vaga_id)
        if not vaga:
            raise ValueError("Vaga não encontrada no banco de dados.")
        return vaga
    
    @staticmethod
    def get_vaga(titulo):
        """ Busca uma vaga pelo titulo. """
        vaga = db.session.query(Vaga).filter_by(titulo=titulo).first()
        if not vaga:
            raise ValueError("Vaga não encontrada no banco de dados.")
        return vaga
    
    @staticmethod
    def get_vagas_by_parcial_titulo(titulo_parcial):
        """ Busca tilulo que contém a palavra digitada. """
          # O % antes e depois indica que o termo pode estar em qualquer parte do texto
        termo_busca = f"%{titulo_parcial}%"
        
        # Usamos .filter() com o operador .ilike() e .all() para trazer uma lista
        vagas = db.session.query(Vaga).filter(Vaga.titulo.ilike(termo_busca)).all()
        
        if not vagas:
            raise ValueError("Vaga não encontrada no banco de dados.")
        return vagas
    @staticmethod

    def get_vaga_by_palavra_chave(palavra_chave):
        """ Busca vagas que contém a palavra chave digitada. """
        termo_busca = f"%{palavra_chave}%"
        vagas = db.session.query(Vaga).filter(Vaga.palavra_chave.ilike(termo_busca)).all()
        
        if not vagas:
            raise ValueError("Vaga não encontrada no banco de dados.")
        return vagas
    
    @staticmethod
    def get_vagas():
        """ Busca todas as vagas. """
        vagas = db.session.query(Vaga).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def get_vagas_by_recrutador(recrutador_id):
        """ Busca todas as vagas de um recrutador específico. """
        vagas = db.session.query(Vaga).options(joinedload(Vaga.recrutador)).filter_by(recrutador_id=recrutador_id).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def get_vagas_by_cidade(cidade):
        """ Busca todas as vagas por cidade. """
        vagas = db.session.query(Vaga).filter_by(cidade=cidade).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def get_vagas_by_uf(uf):
        """ Busca todas as vagas por UF. """
        vagas = db.session.query(Vaga).filter_by(uf=uf).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
            
    @staticmethod
    def get_vagas_by_periodo(data_inicio, data_fim):
        """ Busca todas as vagas entre duas datas.""" 
        vagas = db.session.query(Vaga).filter(Vaga.data_criacao.between(data_inicio, data_fim)).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def listar_vagas_presencial():
        """ Busca todas as vagas presenciais. """
        vagas = db.session.query(Vaga).filter_by(modalidade=Modalidade.PRESENCIAL).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def listar_vagas_hibrido():
        """ Busca todas as vagas híbridas. """
        vagas = db.session.query(Vaga).filter_by(modalidade=Modalidade.HIBRIDO).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def listar_vagas_home_office():
        """ Busca todas as vagas home office. """
        vagas = db.session.query(Vaga).filter_by(modalidade=Modalidade.HOME_OFFICE).all()
        if not vagas:
            raise ValueError("Vagas não encontradas")
        return vagas
    
    @staticmethod
    def listar_vagas_ativas():
        """ Busca todas as vagas ativas. """
        vagas = db.session.query(Vaga).filter_by(status=Status.ATIVO).all()
        return vagas
    
    @staticmethod
    def listar_vagas_inativas():
        """ Busca todas as vagas inativas. """
        vagas = db.session.query(Vaga).filter_by(status=Status.INATIVO).all()
        return vagas

    #Atualização
    @staticmethod
    def update_vaga(vaga_id, data):
        """ Atualiza os dados de uma vaga existente. """
        vaga = db.session.get(Vaga, vaga_id)

        if not vaga:
            raise ValueError("Vaga não encontrada no banco de dados.")
        if 'titulo' in data:
            vaga.titulo = data['titulo']
        if 'descricao' in data:
            vaga.descricao = data['descricao']
        if 'cidade' in data:
            vaga.cidade = data['cidade']
        if 'uf' in data:
            vaga.uf = data['uf']
        if 'palavra_chave' in data:
            vaga.palavra_chave = data['palavra_chave']
        if 'modalidade' in data:
            vaga.modalidade = data['modalidade']
      

        db.session.commit()
        return vaga
    
    @staticmethod
    def desativar_vaga(vaga_id):
        """ Desativa uma vaga. """
        vaga = db.session.get(Vaga, vaga_id)
        if not vaga:
            raise ValueError("Vaga não encontrada no banco de dados.")
        if vaga.status == Status.INATIVO:
            raise ValueError("Vaga já está inativa.")
        vaga.status = Status.INATIVO
        db.session.commit()
        return vaga
    
    @staticmethod
    def ativar_vaga(vaga_id):
        """ Ativar uma vaga. """
        vaga = db.session.get(Vaga, vaga_id)
        if not vaga:
            raise ValueError("Vaga não encontrada no banco de dados.")
        if vaga.status == Status.ATIVO:
            raise ValueError("Vaga já está ativa.")
        vaga.status = Status.ATIVO
        db.session.commit()
        return vaga