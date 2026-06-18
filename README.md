# Python — Task Manager API
## FastAPI · Arquitectura en Capas (Layered / N-Tier)

---

## Estructura del proyecto

```
python-fastapi-tasks/
├── main.py                         # Punto de entrada
├── requirements.txt
├── tasks.db                        # Se genera automáticamente
└── app/
    ├── core/
    │   ├── database.py             # Configuración SQLite + sesión
    │   ├── security.py             # JWT + hashing de contraseñas
    │   └── dependencies.py         # Dependencia get_current_user
    ├── models/
    │   ├── user.py                 # Modelo SQLAlchemy: User
    │   └── task.py                 # Modelo SQLAlchemy: Task
    ├── schemas/
    │   ├── user_schema.py          # Pydantic: UserCreate, TokenResponse...
    │   └── task_schema.py          # Pydantic: TaskCreate, TaskUpdate...
    ├── repositories/
    │   ├── user_repository.py      # Acceso a DB para users
    │   └── task_repository.py      # Acceso a DB para tasks
    ├── services/
    │   ├── auth_service.py         # Lógica: register, login
    │   └── task_service.py         # Lógica: CRUD de tareas
    └── routes/
        ├── auth_routes.py          # Endpoints /auth/*
        └── task_routes.py          # Endpoints /tasks/*
```

---

## Flujo de capas

```
Request HTTP
    ↓
routes/       ← recibe el request, valida esquema Pydantic
    ↓
services/     ← lógica de negocio (reglas, validaciones)
    ↓
repositories/ ← queries a la base de datos
    ↓
models/       ← entidades SQLAlchemy (tablas)
    ↓
SQLite (tasks.db)
```

---

## Requisitos previos

- **Python 3.10+** instalado  
  Verifica con: `python --version` o `python3 --version`

---

## Cómo correr el proyecto

### 1. Crea y activa un entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Mac/Linux
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Corre el servidor

```bash
uvicorn main:app --reload
```

El servidor arranca en: **http://localhost:8000**

> La base de datos `tasks.db` se crea automáticamente al primer arranque. No necesitas hacer ninguna migración.

### 4. Verifica que funciona

Abre en tu navegador: **http://localhost:8000**

Deberías ver:
```json
{ "status": "ok", "project": "P1 - FastAPI Layered Architecture" }
```

También puedes explorar la documentación interactiva en: **http://localhost:8000/docs**

---

## Cómo probarlo en Postman

### URL base
```
http://localhost:8000
```

---

### 1. Registrar usuario

**POST** `/auth/register`

Body (JSON):
```json
{
  "email": "usuario@example.com",
  "username": "usuario1",
  "password": "mipassword123"
}
```

---

### 2. Login (obtener token)

**POST** `/auth/login`

Body (JSON):
```json
{
  "email": "usuario@example.com",
  "password": "mipassword123"
}
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

> Copia el `access_token`. Lo necesitas para todos los endpoints de tareas.

---

### 3. Configurar el token en Postman

En cada request de tareas, ve a la pestaña **Authorization**:
- Type: `Bearer Token`
- Token: pega el `access_token` que obtuviste

---

### 4. Crear una tarea

**POST** `/tasks/`

Body (JSON):
```json
{
  "title": "Aprender arquitectura en capas",
  "description": "Estudiar cómo fluyen las capas routes → services → repositories",
  "priority": "high"
}
```

Valores válidos para `priority`: `"low"` · `"medium"` · `"high"`

---

### 5. Listar tareas

**GET** `/tasks/`

Query params opcionales:
- `status` → `pending` · `in_progress` · `done`
- `priority` → `low` · `medium` · `high`
- `skip` → número de registros a saltar (paginación)
- `limit` → máximo de resultados (default 20)

Ejemplo: `GET /tasks/?status=pending&priority=high`

---

### 6. Ver una tarea específica

**GET** `/tasks/{id}`

Ejemplo: `GET /tasks/1`

---

### 7. Actualizar tarea

**PUT** `/tasks/{id}`

Body (JSON) — todos los campos son opcionales:
```json
{
  "title": "Nuevo título",
  "status": "in_progress",
  "priority": "low"
}
```

Valores válidos para `status`: `"pending"` · `"in_progress"` · `"done"`

---

### 8. Eliminar tarea

**DELETE** `/tasks/{id}`

---

## Colección Postman (importar)

Puedes importar esta colección directamente en Postman.  
Guarda el siguiente JSON como `python-tasks.postman_collection.json` e impórtalo:

```json
{
  "info": { "name": "P1 - FastAPI Tasks", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "variable": [
    { "key": "base_url", "value": "http://localhost:8000" },
    { "key": "token", "value": "" }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/auth/register",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\"email\": \"user@example.com\", \"username\": \"user1\", \"password\": \"password123\"}" }
          }
        },
        {
          "name": "Login",
          "event": [{ "listen": "test", "script": { "exec": ["const r = pm.response.json(); pm.collectionVariables.set('token', r.access_token);"] } }],
          "request": {
            "method": "POST",
            "url": "{{base_url}}/auth/login",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\"email\": \"user@example.com\", \"password\": \"password123\"}" }
          }
        }
      ]
    },
    {
      "name": "Tasks",
      "item": [
        {
          "name": "List Tasks",
          "request": { "method": "GET", "url": "{{base_url}}/tasks/", "auth": { "type": "bearer", "bearer": [{ "key": "token", "value": "{{token}}" }] } }
        },
        {
          "name": "Create Task",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/tasks/",
            "auth": { "type": "bearer", "bearer": [{ "key": "token", "value": "{{token}}" }] },
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\"title\": \"Mi primera tarea\", \"description\": \"Descripción aquí\", \"priority\": \"high\"}" }
          }
        },
        {
          "name": "Get Task",
          "request": { "method": "GET", "url": "{{base_url}}/tasks/1", "auth": { "type": "bearer", "bearer": [{ "key": "token", "value": "{{token}}" }] } }
        },
        {
          "name": "Update Task",
          "request": {
            "method": "PUT",
            "url": "{{base_url}}/tasks/1",
            "auth": { "type": "bearer", "bearer": [{ "key": "token", "value": "{{token}}" }] },
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\"status\": \"in_progress\"}" }
          }
        },
        {
          "name": "Delete Task",
          "request": { "method": "DELETE", "url": "{{base_url}}/tasks/1", "auth": { "type": "bearer", "bearer": [{ "key": "token", "value": "{{token}}" }] } }
        }
      ]
    }
  ]
}
```

> El request de Login tiene un script de test que guarda el token automáticamente en la variable `{{token}}` — así no tienes que copiarlo manualmente en cada request.
