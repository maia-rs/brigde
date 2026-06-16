from models.banco import db
from models.user import User
from models.recrutador import Recrutador
from sqlalchemy.orm import joinedload



class RecrutadorService:
    """ Serviço para gerenciar operações de recrutadores. """

    # Criação de Recrutador
    @staticmethod
    def create_recrutador(data, usuario_id):
        """ Cria um novo Recrutador. """
        #1 Verifica se existe o recrutador

        recrutador_existente = db.session.query(Recrutador).filter_by(usuario_id=usuario_id).first()

        if recrutador_existente:
            # Se encontrou, impede o cadastro disparando a exceção
            raise ValueError("Este usuário já possui um recrutador cadastrado.")
        
        # 2. Se não encontrou, o fluxo continua normalmente para o cadastro

        recrutador = Recrutador(
            usuario_id=usuario_id,
            empresa=data['empresa'],
            
        )
     

        db.session.add(recrutador)
        db.session.commit()
        return recrutador
    
    # Buscas
    @staticmethod
    def get_recrutador_by_id(recrutador_id):
        """ Busca um recrutador pelo ID, trazendo todas as suas infos """
        recrutador = (
    db.session.query(Recrutador)               # 1. Abre a consulta no modelo Recrutador
    .options(joinedload(Recrutador.usuario))   # 2. Carrega a classe User associada
    .filter_by(id=recrutador_id)               # 3. Filtra pelo ID do recrutador
    .first()                                   # 4. Executa e traz o primeiro resultado
)
        if not recrutador:
            raise ValueError("Recrutador não encontrado no banco de dados.")
        return recrutador
    
    @staticmethod
    def get_recrutadores():
        """ Busca todos os recrutadores, trazendo todas as suas infos """
        recrutadores = db.session.query(Recrutador).options(joinedload(Recrutador.usuario)).all()
        return recrutadores

    @staticmethod
    def get_recrutador(nome):
        """ Busca um recrutador pelo nome. """
        recrutador= (
    db.session.query(Recrutador)
    .join(Recrutador.usuario)  # 1. Faz o JOIN com a tabela de usuários
    .filter(User.nome == nome)  # 2. Filtra usando o modelo Usuario 
    .options(joinedload(Recrutador.usuario))  # 3. Mantém o carregamento ansioso para evitar novas consultas depois
    .first()
)
        if not recrutador:
            raise ValueError("Recrutador não encontrado no banco de dados.")
        return recrutador
    
    @staticmethod
    def get_recrutadores_by_empresa(empresa):
        """ Busca todos recrutadores por empresa. """
        recrutadores = db.session.query(Recrutador).filter_by(empresa=empresa).all()
        return recrutadores
    
   
    
    # Atualização
    @staticmethod
    def update_recrutador(recrutador_id, data):
        """ Atualiza os dados de um candidato existente. """
        recrutador = db.session.get(Recrutador, recrutador_id) 

        if not recrutador:
            raise ValueError("Recrutador não encontrado no banco de dados.")

        if 'empresa' in data:
            recrutador.empresa = data['empresa']
      
        db.session.commit()
        return recrutador


   