# 🛒 Marketplace - Django REST & Vue 3

Un marketplace full-stack construido con Django REST Framework, Autenticación JWT, y Vue 3 como frontend.

Permite registro, login, gestión de productos con imágenes y CRUD completo por usuario.

---

## 🚀 Tecnologías usadas

### Backend – Django REST Framework
- Python 3
- Django 4
- Django REST Framework
- JWT (SimpleJWT)
- SQLite3
- Pillow (para imágenes)

### Frontend – Vue 3
- Vite
- Axios
- Vue Router
- LocalStorage para tokens

---

## ✨ Funcionalidades

### 👤 Usuarios
- Registro con email + username + password
- Login con JWT (access + refresh)
- `GET /users/me/` para obtener usuario autenticado

### 🛍️ Productos
- Crear productos con imagen
- Listar todos los productos
- Ver detalle
- Editar y eliminar solo si eres el propietario
- **Protecciones con permisos:**
  - `GET` → público
  - `POST / PUT / DELETE` → solo autenticado

---

## 📦 Instalación Backend

```bash
cd backend
python -m venv venv
venv/Scripts/activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Rutas API principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/users/register/` | Registro |
| POST | `/api/users/login/` | Login (JWT) |
| GET | `/api/users/me/` | Usuario autenticado |
| GET | `/api/products/` | Listar productos |
| POST | `/api/products/` | Crear producto |
| GET | `/api/products/<id>/` | Ver detalle |
| PUT | `/api/products/<id>/` | Actualizar |
| DELETE | `/api/products/<id>/` | Eliminar |

---

## 🎨 Instalación Frontend

```bash
cd frontend
npm install
npm run dev
```

### Configuración Axios

```javascript
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});
```

---

## 🖼️ Subida de imágenes

Asegúrate de tener configurado en `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Y en `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔐 Autenticación

El token se guarda en `localStorage`:

```javascript
localStorage.setItem("access", token);
axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
```

---

## 📄 Pendiente / Mejoras futuras


---

## 📜 Licencia

Libre para uso educativo o portfolio.

---

*Si quieres te genero también un logo simple, un badge pack, o una versión más larga/profesional del README.*
