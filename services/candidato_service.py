from models.banco import db
from models.user import User
from models.candidato import Candidato
from sqlalchemy.orm import joinedload
from datetime import date, datetime





class CandidatoService:
    """ Serviço para gerenciar operações de ucandidatos. """

    # Criação de Candidato
    @staticmethod
    
    def create_candidato(data,user_id):
        """ Cria um novo candidato. """

        #1 Verifica se o candidato já existe
        candidato_existente = db.session.query(Candidato).filter_by(user_id=user_id).first()

        if candidato_existente:
            # Se encontrou, impede o cadastro disparando a exceção
            raise ValueError("Este usuário já possui um candidato cadastrado.")
        
        data_nascimento_texto = data.get('data_nascimento')
        try:
            data_nascimento_objeto = datetime.strptime(data_nascimento_texto, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValueError("Formato de data inválido. Use o padrão AAAA-MM-DD.")
        
        #2 Se não continua
        candidato = Candidato(
            user_id=user_id,
            cidade=data['cidade'],
            uf=data['uf'],
            telefone=data['telefone'],
            palavra_chave=data['palavra_chave'],
            profissao=data['profissao'],
            data_nascimento=data_nascimento_objeto
        )
        db.session.add(candidato)
        db.session.commit()
        return candidato
    
    # Buscas
    @staticmethod
    def get_candidato_by_id(candidato_id):
        """ Busca um candidato pelo ID, trazendo todas as suas infos """
        candidato= (
        db.session.query(Candidato)               # 1. Abre a consulta no modelo 
        .options(joinedload(Candidato.usuario))   # 2. Carrega a classe User associada
        .filter_by(id=candidato_id)               # 3. Filtra pelo ID
        .first()                                   # 4. Executa e traz o primeiro resultado
    )
        if not candidato:
            raise ValueError("Candidato não encontrado no banco de dados.")
        return candidato
    
    @staticmethod
    def get_candidatos():
        """ Busca todos os candidatos, trazendo todas as suas infos """
        candidatos = db.session.query(Candidato).options(joinedload(Candidato.usuario)).all()
        return candidatos

    @staticmethod
    def get_candidato(nome):
        """ Busca um candidato pelo nome. """
        candidato= (
    db.session.query(Candidato)
    .join(Candidato.usuario)  # 1. Faz o JOIN com a tabela de usuários
    .filter(User.nome == nome)  # 2. Filtra usando o modelo Usuario 
    .options(joinedload(Candidato.usuario))  # 3. Mantém o carregamento ansioso para evitar novas consultas depois
    .first()
)
        if not candidato:
            raise ValueError("Candidato não encontrado no banco de dados.")
        return candidato
    

    @staticmethod
    def get_candidatos_by_palavra_chave(palavra_chave):
        """ Busca candidatos que contém a palavra chave digitada. """
        termo_busca = f"%{palavra_chave}%"
        candidatos = db.session.query(Candidato).filter(Candidato.palavra_chave.ilike(termo_busca)).all()
        
        if not candidatos:
            raise ValueError("Candidato não encontrada no banco de dados.")
        return candidatos
    

    @staticmethod
    def get_candidatos_by_cidade(cidade):
        """ Busca todos candidatos por cidade. """
        candidatos = db.session.query(Candidato).filter_by(cidade=cidade).all()
        return candidatos
    
    @staticmethod
    def get_candidatos_by_uf(uf):
        """ Busca todos candidatos por UF. """
        candidatos = db.session.query(Candidato).filter_by(uf=uf).all()
        return candidatos
    
    @staticmethod
    def get_candidatos_by_profissao(profissao):
        """ Busca todos candidatos por profissão. """
        candidatos = db.session.query(Candidato).filter_by(profissao=profissao).all()
        return candidatos
    
    

    @staticmethod
    def get_candidatos_by_idade(idade):
        """ Busca todos candidatos por idade calculando o intervalo de nascimento. """
        hoje = date.today()
        
        # Menor data possível de nascimento para quem tem essa idade (ex: fez aniversário hoje)
        data_inicio = hoje.replace(year=hoje.year - idade - 1) + datetime.timedelta(days=1)
        
        # Maior data possível de nascimento para quem tem essa idade
        data_fim = hoje.replace(year=hoje.year - idade)
        
        # O banco de dados filtra rapidamente usando o índice da coluna de data
        candidatos = db.session.query(Candidato).filter(
            Candidato.data_nascimento.between(data_inicio, data_fim)
        ).all()
        
        return candidatos


    @staticmethod
    def get_candidatos_by_data_nascimento(data_nascimento):
        """ Busca todos candidatos por data de nascimento. """
        candidatos = db.session.query(Candidato).filter_by(data_nascimento=data_nascimento).all()
        return candidatos
   
   
    # Atualização
    @staticmethod
    def update_candidato(candidato_id, data):
        """ Atualiza os dados de um candidato existente. """
        candidato = db.session.get(Candidato, candidato_id) 

        if not candidato:
            raise ValueError("Candidato não encontrado no banco de dados.")

        if 'cidade' in data:
            candidato.cidade = data['cidade']
        if 'uf' in data:
            candidato.uf = data['uf']
        if 'telefone' in data:
            candidato.telefone = data['telefone']
        if 'palavra_chave' in data:
            candidato.palavra_chave = data['palavra_chave']
        if 'profissao' in data:
            candidato.profissao = data['profissao']
        if 'data_nascimento' in data:
            candidato.data_nascimento = data['data_nascimento']

        db.session.commit()
        return candidato

   

   