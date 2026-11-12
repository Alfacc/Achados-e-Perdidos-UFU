# Achados e Perdidos UFU

Plataforma web para a comunidade da UFU registrar objetos perdidos e encontrados nos campi.

**Stack:** Vue 3 (Vite) + Django REST Framework + SQLite, com autenticação por JWT.

## Sprints

### Sprint 1: ajustes iniciais
Repositório, escolha das tecnologias, definição do sistema e backlog.

### Sprint 2
- **SCRUM-10**: cadastro e login com e-mail UFU
- **SCRUM-12**: cadastrar objeto perdido
  - SCRUM-23: modelar e criar a tabela de Item no SQLite
  - SCRUM-24: serializer e endpoint (POST) do objeto perdido
  - SCRUM-25: interface do formulário "Perdi um objeto"
  - SCRUM-26: conexão do formulário com a API via Axios e tratamento de erros
- **Cadastrar objeto encontrado**: botão "Encontrei um objeto" na página inicial, usando o mesmo formulário (modal) do objeto perdido com `type=FOUND`

### Backlog
| Ticket | História |
|---|---|
| SCRUM-13 | Ver uma lista de objetos cadastrados |
| SCRUM-14 | Filtrar objetos por categoria |
| SCRUM-15 | Comunicar-se com o dono de um objeto que encontrei |
| SCRUM-16 | Comunicar-se com quem achou meu objeto |
| SCRUM-17 | Marcar um objeto perdido/encontrado como devolvido |
| SCRUM-18 | Ser notificado se um objeto parecido com o que perdi for encontrado |

O modelo `Item` tem `type` (`LOST`/`FOUND`), `status` (`OPEN`/`RESOLVED`) e `category`,
usados pelos cadastros de objeto perdido e encontrado e que servem de base para as SCRUM-13, 14 e 17.

## Como rodar

Pré-requisitos: Python 3.10+ e Node.js 18+.

### Back-end (terminal 1)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser # opcional, para usar /admin
python manage.py runserver       # API em http://localhost:8000/api/
```

### Front-end (terminal 2)
```bash
cd frontend
cp .env.example .env             # opcional: o padrão já aponta para localhost:8000
npm install
npm run dev                      # http://localhost:5173
```

Acesse o sistema em **http://localhost:5173**. A porta 8000 serve só a API (`/api/`) e o
painel administrativo (`/admin/`), por isso `http://localhost:8000/` retorna 404.

### Testes do back-end
```bash
cd backend
python manage.py test
```

## Endpoints

Rotas marcadas com 🔒 exigem o cabeçalho `Authorization: Bearer <access token>`.

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/register/` | Cadastro (apenas e-mail UFU) |
| POST | `/api/auth/login/` | Login → `access`, `refresh`, `user` |
| POST | `/api/auth/token/refresh/` | Renova o access token |
| GET 🔒 | `/api/auth/me/` | Usuário logado |
| GET 🔒 | `/api/categories/` | Lista de categorias |
| GET 🔒 | `/api/items/` | Lista de objetos (mais recentes primeiro) |
| POST 🔒 | `/api/items/` | Cadastra objeto (`multipart/form-data` quando houver foto) |
| GET 🔒 | `/api/items/<id>/` | Detalhe de um objeto |

## Regras de validação

**Conta**
- E-mail dos domínios em `ALLOWED_EMAIL_DOMAINS` (hoje `ufu.br`, incluindo subdomínios como `discente.ufu.br`), sem diferenciar maiúsculas.
- Senha com pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número.

**Objeto**
- Título com até 120 caracteres, local com até 150 e descrição com até 1000.
- A data em que o objeto foi perdido/encontrado não pode estar no futuro.
- Foto opcional, apenas imagem, com até `MAX_PHOTO_MB` (5 MB).
- `owner` e `status` são definidos pelo servidor (usuário logado e `OPEN`) e não podem ser enviados pelo cliente.

## Configurações

**Back-end** (`backend/config/settings.py`)
- `ALLOWED_EMAIL_DOMAINS`: domínios aceitos no cadastro. Para testar sem e-mail UFU em desenvolvimento, adicione temporariamente `"gmail.com"`.
- `MAX_PHOTO_MB`: tamanho máximo da foto.
- Variáveis de ambiente: `DJANGO_SECRET_KEY` (obrigatória em produção), `DJANGO_DEBUG` (`1`/`0`) e `DJANGO_ALLOWED_HOSTS` (separados por vírgula).

**Front-end** (`frontend/.env`)
- `VITE_API_URL`: endereço da API (padrão `http://localhost:8000/api`).

## Estrutura

```
backend/
  accounts/   usuário com login por e-mail, cadastro, login JWT
  items/      categorias e objetos (Item), com as categorias iniciais criadas via migration
  config/     settings e rotas
frontend/src/
  views/      Login, Cadastro e Home (lista de objetos)
  components/ modal de cadastro de objeto (perdido ou encontrado) e layout das telas de acesso
  services/   cliente Axios com renovação automática do token
  stores/     estado de autenticação (Pinia)
```
