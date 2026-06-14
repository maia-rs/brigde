from models.banco import db
from models.user import User
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
        if db.session.query(User).filter_by(email=data['email']).first():
            raise ValueError("Este e-mail já está cadastrado no sistema.")
            
        # 2° Criptografa a senha        
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
            raise ValueError("Candidato não encontrado no banco de dados.")
        return usuario
   
    @staticmethod
    def get_usuarios():
        """ Busca todos os usuários. """
        usuarios = db.session.query(User).all()
        return usuarios
    
    @staticmethod
    def get_usuarios_by_status(status):
        """ Busca todos os usuários por status. """
        usuarios = db.session.query(User).filter_by(status=status).all()
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
            if db.session.query(User).filter_by(email=data['email']).first():
                raise ValueError("Este e-mail já está cadastrado no sistema.")
            usuario.email = data['email']
        if 'senha' in data:
            usuario.senha = generate_password_hash(data['senha'])
        if 'status' in data:
            usuario.status = data['status']
            
        db.session.commit()
        return usuario

    # Login
    @staticmethod
    def verify_login(email_or_nome, senha):
        """ Verifica as credenciais de login aceitando e-mail ou nome. """
        usuario = db.session.query(User).filter(
            (User.email == email_or_nome) | (User.nome == email_or_nome)
        ).first()
        
        # Se encontrou o usuário e a senha do Werkzeug bater, retorna o objeto
        if usuario and check_password_hash(usuario.senha, senha):
            return usuario
            
        # Caso contrário, levanta um erro para a rota tratar
        raise ValueError("Usuário ou senha incorretos.")
