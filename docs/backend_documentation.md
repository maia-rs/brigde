# Documentação do Backend - Banco de Talentos

O backend do projeto "Banco de Talentos" é uma API RESTful baseada em Flask, projetada para gerenciar dados de usuários, candidatos, recrutadores, vagas de emprego e candidaturas. Ele segue uma arquitetura em camadas para garantir a separação de responsabilidades, manutenibilidade e escalabilidade.

## 1. Visão Geral da Arquitetura

O backend é organizado em três camadas principais:

*   **Rotas (`routes/`)**: Esta camada define os endpoints da API. É responsável por receber requisições HTTP, validar os dados de entrada usando schemas Pydantic, invocar a lógica de negócio apropriada da camada de `services` e formatar as respostas HTTP (JSON). Blueprints do Flask são usados para agrupar rotas relacionadas, melhorando a modularidade.
*   **Serviços (`services/`)**: Esta camada encapsula a lógica de negócio central da aplicação. As classes de serviço interagem diretamente com os modelos do banco de dados, realizam manipulação de dados, aplicam regras de negócio (por exemplo, verificações de unicidade, transições de status, hash de senhas) e tratam exceções específicas relacionadas ao negócio. Elas são projetadas para serem independentes do ciclo de requisição/resposta HTTP.
*   **Schemas (`schemas/`)**: Esta camada utiliza modelos Pydantic para definir a estrutura e as regras de validação tanto para os payloads de requisição de entrada quanto para as respostas da API de saída. Os schemas garantem a integridade dos dados, fornecem contratos de dados claros para a API e facilitam a serialização/desserialização automática de objetos Python para/de JSON.
*   **Modelos (`models/`)**: (Implicitamente, pois `models.banco` e outras classes de modelo são importadas) Esta camada define os modelos ORM do SQLAlchemy, que representam as tabelas do banco de dados e seus relacionamentos. Ela lida com a persistência dos dados no banco de dados.

## 2. Tecnologias Chave

*   **Flask**: O micro-framework utilizado para construir a API web.
*   **Flask-JWT-Extended**: Fornece suporte robusto para autenticação baseada em JSON Web Token (JWT), protegendo os endpoints da API.
*   **SQLAlchemy**: Um Mapeador Objeto-Relacional (ORM) que permite que objetos Python interajam com o banco de dados, abstraindo as consultas SQL.
*   **Pydantic**: Uma biblioteca de validação e parsing de dados usada para definir formatos de dados e impor regras de validação.
*   **Werkzeug Security**: Utilizado para hash e verificação segura de senhas.

## 3. Autenticação e Autorização

*   **JWT (JSON Web Tokens)**: O sistema usa JWTs para autenticação sem estado. Após o login bem-sucedido do usuário, um `access_token` é emitido. Este token deve ser incluído no cabeçalho `Authorization` (por exemplo, `Authorization: Bearer <token>`) para todas as requisições subsequentes a endpoints protegidos.
*   **`@jwt_required()`**: Este decorador do `Flask-JWT-Extended` é usado para proteger rotas, garantindo que apenas requisições com um JWT válido possam acessá-las. (Nota: No código fornecido, este decorador está comentado em muitas rotas, o que implica que é para desenvolvimento ou temporariamente desabilitado).
*   **Segurança de Senha**: As senhas dos usuários nunca são armazenadas diretamente. `werkzeug.security.generate_password_hash` é usado para fazer o hash das senhas antes do armazenamento, e `check_password_hash` é usado para verificá-las com segurança durante as tentativas de login.

## 4. Tratamento de Erros

O backend emprega uma abordagem estruturada para o tratamento de erros:

*   **`ValueError`**: Esta exceção é levantada pela camada de `services` para falhas de validação da lógica de negócio (por exemplo, um usuário tentando se candidatar à mesma vaga duas vezes, um recurso não encontrado durante uma atualização, formato de dados inválido para uma regra de negócio específica). Elas são capturadas na camada de `routes` e geralmente resultam em uma resposta HTTP `422 Unprocessable Entity`, fornecendo uma mensagem de erro clara ao cliente.
*   **`Exception` (Geral)**: Um bloco `except Exception as e` amplo é usado para capturar quaisquer erros inesperados que possam ocorrer durante o processamento da requisição, incluindo problemas de banco de dados ou erros de tempo de execução não tratados. Estes resultam em uma resposta HTTP `500 Internal Server Error`. Crucialmente, `db.session.rollback()` é chamado dentro desses blocos para garantir que quaisquer transações de banco de dados incompletas sejam revertidas, mantendo a consistência dos dados.
*   **Erros de Validação Pydantic**: Quando `Pydantic.model_validate()` falha devido a dados de entrada malformados, ele levanta um `ValidationError` (que é uma subclasse de `ValueError`). Estes são capturados pelo manipulador de `ValueError` nas rotas e retornados como respostas `422`.

## 5. Detalhamento dos Módulos

### 5.1. `routes/` - Endpoints da API

Este diretório contém Blueprints do Flask, cada um gerenciando um conjunto de endpoints da API relacionados.

*   **`user_routes.py`**
    *   **Propósito**: Gerencia o registro de usuários, login e gerenciamento de perfil.
    *   **Endpoints**:
        *   `POST /usuario`: Registra um novo usuário.
        *   `POST /login`: Autentica o usuário e emite JWT.
        *   `GET /usuario/<int:user_id>`: Recupera um usuário por ID.
        *   `GET /usuario`: Lista todos os usuários.
        *   `GET /usuario/ativos`: Lista usuários ativos.
        *   `GET /usuario/inativos`: Lista usuários inativos.
        *   `PUT /usuario/<int:user_id>`: Atualiza os detalhes do usuário.

*   **`candidato_routes.py`**
    *   **Propósito**: Gerencia a criação, recuperação e funcionalidades de busca de perfis de candidatos.
    *   **Endpoints**:
        *   `POST /candidato/<int:user_id>`: Cria um perfil de candidato para um usuário.
        *   `GET /candidato/<int:candidato_id>`: Recupera um perfil de candidato por ID.
        *   `GET /candidatos`: Lista todos os perfis de candidatos.
        *   `GET /candidato/busca_nome?nome=<name>`: Busca candidatos por nome.
        *   `GET /candidato/palavra_chave?palavra=<keyword>`: Busca candidatos por palavra-chave.
        *   `GET /candidato/cidade?cidade=<city>`: Busca candidatos por cidade.
        *   `GET /candidato/uf?uf=<uf>`: Busca candidatos por estado (UF).
        *   `GET /candidato/profissao?profissao=<profession>`: Busca candidatos por profissão.
        *   `GET /candidato/idade/<int:idade>`: Busca candidatos por idade.
        *   `GET /candidato/data_nascimento?data=<YYYY-MM-DD>`: Busca candidatos por data de nascimento.
        *   `PUT /candidato/<int:candidato_id>`: Atualiza o perfil do candidato.

*   **`candidatura_routes.py`**
    *   **Propósito**: Gerencia a criação, recuperação e atualização de status de candidaturas a vagas.
    *   **Endpoints**:
        *   `POST /candidatura/<int:vaga_id>/<int:candidato_id>`: Cria uma nova candidatura a vaga.
        *   `GET /candidatura/<int:candidatura_id>`: Recupera uma candidatura por ID.
        *   `GET /candidatura/candidato/<int:candidato_id>`: Lista candidaturas de um candidato específico.
        *   `GET /candidatura/periodo?data_inicio=<YYYY-MM-DD>&data_fim=<YYYY-MM-DD>`: Busca candidaturas por período de criação.
        *   `GET /candidatura/status?status=<status>`: Busca candidaturas por status.
        *   `PUT /candidatura/enviada/<int:candidatura_id>`: Atualiza o status para 'ENVIADA'.
        *   `PUT /candidatura/em_analise/<int:candidatura_id>`: Atualiza o status para 'EM_ANALISE'.
        *   `PUT /candidatura/entrevista/<int:candidatura_id>`: Atualiza o status para 'ENTREVISTA'.
        *   `PUT /candidatura/aprovada/<int:candidatura_id>`: Atualiza o status para 'APROVADA'.
        *   `PUT /candidatura/reprovada/<int:candidatura_id>`: Atualiza o status para 'REPROVADA'.

*   **`recrutador_routes.py`**
    *   **Propósito**: Gerencia a criação, recuperação e funcionalidades de busca de perfis de recrutadores.
    *   **Endpoints**:
        *   `POST /recrutador/<int:user_id>`: Cria um perfil de recrutador para um usuário.
        *   `GET /recrutador/<int:recrutador_id>`: Recupera um perfil de recrutador por ID.
        *   `GET /recrutador`: Lista todos os perfis de recrutadores.
        *   `GET /recrutador/busca_nome?nome=<name>`: Busca recrutadores por nome.
        *   `GET /recrutador/empresa?empresa=<company>`: Busca recrutadores por empresa.
        *   `PUT /recrutador/<int:recrutador_id>`: Atualiza o perfil do recrutador.

*   **`vagas_routes.py`**
    *   **Propósito**: Gerencia a criação, recuperação, busca e gerenciamento de status de vagas de emprego.
    *   **Endpoints**:
        *   `POST /vaga/<int:recrutador_id>`: Cria uma nova vaga de emprego.
        *   `GET /vaga/<int:vaga_id>`: Recupera uma vaga por ID.
        *   `GET /vaga`: Lista todas as vagas.
        *   `GET /vaga/titulo_parcial?titulo_parcial=<title_part>`: Busca vagas por título parcial.
        *   `GET /vaga/palavra_chave?palavra_chave=<keyword>`: Busca vagas por palavra-chave.
        *   `GET /vaga/recrutador/<int:recrutador_id>`: Lista vagas por recrutador.
        *   `GET /vaga/cidade?cidade=<city>`: Busca vagas por cidade.
        *   `GET /vaga/uf?uf=<uf>`: Busca vagas por estado (UF).
        *   `GET /vaga/periodo?data_inicio=<YYYY-MM-DD>&data_fim=<YYYY-MM-DD>`: Busca vagas por período de criação.
        *   `GET /vaga/modalidade/presencial`: Lista vagas presenciais.
        *   `GET /vaga/modalidade/hibrida`: Lista vagas híbridas.
        *   `GET /vaga/modalidade/homeoffice`: Lista vagas home office.
        *   `GET /vaga/status/aberta`: Lista vagas ativas.
        *   `GET /vaga/status/fechada`: Lista vagas inativas.
        *   `PUT /vaga/<int:vaga_id>`: Atualiza os detalhes da vaga.
        *   `PUT /vaga/desativar/<int:vaga_id>`: Desativa uma vaga.
        *   `PUT /vaga/ativar/<int:vaga_id>`: Ativa uma vaga.

### 5.2. `services/` - Lógica de Negócio

Este diretório contém classes que encapsulam a lógica de negócio para cada domínio.

*   **`user_service.py`**
    *   **Classe**: `UsuarioService`
    *   **Responsabilidades**: Criação de usuário (com hash de senha e verificação de unicidade de e-mail), recuperação, gerenciamento de status (ativo/inativo) e verificação de login.

*   **`candidato_service.py`**
    *   **Classe**: `CandidatoService`
    *   **Responsabilidades**: Criação de perfil de candidato (verificando perfis existentes), recuperação (por ID, nome, palavra-chave, localização, profissão, idade, data de nascimento) e atualizações. Inclui lógica para calcular a idade a partir da data de nascimento.

*   **`recrutador_service.py`**
    *   **Classe**: `RecrutadorService`
    *   **Responsabilidades**: Criação de perfil de recrutador (verificando perfis existentes), recuperação (por ID, nome, empresa) e atualizações.

*   **`vaga_service.py`**
    *   **Classe**: `VagaService`
    *   **Responsabilidades**: Criação de vaga de emprego, recuperação (por ID, título, palavra-chave, recrutador, localização, período, modalidade, status) e gerenciamento de status (ativar/desativar).

*   **`candidatura_service.py`**
    *   **Classe**: `CandidaturaService`
    *   **Responsabilidades**: Criação de candidatura a vaga (verificando duplicatas e status de vaga ativa), recuperação (por ID, candidato, vaga, período, status) e transições de status (enviada, em_analise, entrevista, aprovada, reprovada).

### 5.3. `schemas/` - Validação e Serialização de Dados

Este diretório define modelos Pydantic para validação e serialização de dados.

*   **`user_schema.py`**
    *   `CreateUser`: Define campos para criação de usuário (nome, email, password).
    *   `GetUser`: Define campos para recuperação de usuário (id, name, email, status).
    *   `UpdateUser`: Define campos opcionais para atualização de usuário.
    *   `Login`: Define campos para login de usuário (email, password).

*   **`candidato_schema.py`**
    *   `CreateCandidato`: Define campos para criação de perfil de candidato (city, uf, telefone, palavra_chave, profissao, data_nascimento).
    *   `GetCandidato`: Define campos para recuperação de perfil de candidato, incluindo `GetUser` aninhado para detalhes do usuário.
    *   `UpdateCandidato`: Define campos opcionais para atualização de perfil de candidato.

*   **`recrutador_schema.py`**
    *   `CreateRecrutador`: Define campos para criação de perfil de recrutador (empresa).
    *   `GetRecrutador`: Define campos para recuperação de perfil de recrutador, incluindo `GetUser` aninhado para detalhes do usuário.
    *   `UpdateRecrutador`: Define campos opcionais para atualização de perfil de recrutador.

*   **`vagas_schema.py`**
    *   `CreateVaga`: Define campos para criação de vaga de emprego (titulo, descricao, cidade, uf, palavra_chave, modalidade).
    *   `GetVaga`: Define campos para recuperação de vaga de emprego, incluindo `GetRecrutador` aninhado para detalhes do recrutador.
    *   `UpdateVaga`: Define campos opcionais para atualização de vaga de emprego.

*   **`candidatura_schema.py`**
    *   `CreateCandidatura`: Um schema vazio, indicando que a lógica de criação depende de parâmetros de caminho em vez de um corpo de requisição.
    *   `GetCandidatura`: Define campos para recuperação de candidatura a vaga, incluindo `GetCandidato` e `GetVaga` aninhados para informações detalhadas.
    *   `UpdateCandidatura`: Define campos opcionais para atualização de status de candidatura a vaga.