from models.banco import db
from models.user import User, Status
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_ # Importante para a lógica de "OU" no login
from sqlalchemy.orm import joinedload

class UsuarioService: 
    """ Serviço para gerenciar operações de usuários. """

    # Criação usuário
    @staticmethod
    def create_usuario(data):
        """ Cria um novo usuário com senha criptografada. """
        # 1º Verifica se e-mail já existe
        if db.session.query(User.id).filter_by(email=data['email']).first():
            raise ValueError("Este e-mail já está cadastrado no sistema.")
                         
        #2° Criptografa a senha        
        hashed_password = generate_password_hash(data['senha'])

        # 3° Cria o usuário
        novo_usuario = User(
            nome=data['nome'],
            email=data['email'],
            senha=hashed_password
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    # Buscas
    @staticmethod
    def get_usuario_by_id(usuario_id):
        """ Busca um usuário pelo ID. """
        usuario = db.session.get(User,usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado no banco de dados.")
        return usuario
   
    @staticmethod
    def get_usuarios():
        """ Busca todos os usuários. """
        usuarios = db.session.query(User).all()
        return usuarios
    
    @staticmethod
    def listar_usuarios_ativos():
        """ Busca todos os usuários ativos. """
        usuarios = db.session.query(User).filter_by(status=Status.ATIVO).all()
        return usuarios
    
    @staticmethod
    def listar_usuarios_inativos():
        """ Busca todos os usuários inativos. """
        usuarios = db.session.query(User).filter_by(status=Status.INATIVO).all()
        return usuarios
       

    # Atualização
    @staticmethod
    def update_usuario(usuario_id, data):
        """ Atualiza os dados de um usuário existente. """
        usuario = db.session.get(User, usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado no banco de dados.") 
        
        if 'nome' in data:
            usuario.nome = data['nome']
        if 'email' in data:
            if 'email' in data and data['email'] != usuario.email:
                # Verifica se o novo e-mail já pertence a OUTRO usuário
                email_existe = db.session.query(User.id).filter(
                User.email == data['email'], 
                User.id != usuario.id
                ).first() is not None

            if email_existe:
                raise ValueError("Este e-mail já está cadastrado no sistema.")
        
            usuario.email = data['email']
        if 'senha' in data:
            usuario.senha = generate_password_hash(data['senha'])
       
            
        db.session.commit()
        return usuario
    
    @staticmethod
    def desativar_usuario(usuario_id):
        """ Desativa um usuário. """
        usuario = db.session.get(User, usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado no banco de dados.")
        if usuario.status == Status.INATIVO:
            raise ValueError("Usuário já está inativo.")
        usuario.status = Status.INATIVO
        db.session.commit()
        return usuario
    
    @staticmethod
    def ativar_usuario(usuario_id):
        """ Ativar um usuário. """
        usuario = db.session.get(User, usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado no banco de dados.")
        if usuario.status == Status.ATIVO:
            raise ValueError("Usuário já está ativo.")
        usuario.status = Status.ATIVO
        db.session.commit()
        return usuario
    

    # Login
    @staticmethod
    def verify_login(email, senha):
        """ Verifica as credenciais de login aceitando e-mail. """
        usuario = db.session.query(User).filter(
            (User.email == email) 
        ).first()       
        
        # Se encontrou o usuário e a senha do Werkzeug bater, retorna o objeto
        if not usuario or not check_password_hash(usuario.senha, senha):
            raise ValueError("Usuário ou senha incorretos.")
        
         #Verifica se usuário está ativo
        if usuario.status != Status.ATIVO:
            raise ValueError("Usuário inativo.")
        
        #Sucesso 
        return usuario