# Achados e Perdidos UFU

Vue 3 (Vite) + Django REST Framework + SQLite.

## Sprint 1
- **SCRUM-10** – Cadastro e login com e-mail UFU
- **SCRUM-12** – Cadastrar objeto perdido

## Como rodar

### Back-end (terminal 1)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser # opcional, para usar /admin
python manage.py runserver       # http://localhost:8000
```

### Front-end (terminal 2)
```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

### Testes do back-end
```bash
cd backend
python manage.py test
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/register/` | Cadastro (apenas e-mail UFU) |
| POST | `/api/auth/login/` | Login → `access`, `refresh`, `user` |
| POST | `/api/auth/token/refresh/` | Renova o access token |
| GET | `/api/auth/me/` | Usuário logado |
| GET | `/api/categories/` | Lista de categorias |
| GET/POST | `/api/items/` | Lista / cadastra objeto (`multipart/form-data`) |

## Configurações úteis (`backend/config/settings.py`)
- `ALLOWED_EMAIL_DOMAINS`: domínios aceitos no cadastro (hoje `ufu.br`, aceitando subdomínios).
- `MAX_PHOTO_MB`: tamanho máximo da foto.
- Para testar sem e-mail UFU em desenvolvimento, adicione temporariamente `"gmail.com"` à lista.

## Próximas histórias
O modelo `Item` já tem `type` (`LOST`/`FOUND`), `status` (`OPEN`/`RESOLVED`) e `category`,
então SCRUM-11, 13, 14 e 17 reaproveitam o que existe.
