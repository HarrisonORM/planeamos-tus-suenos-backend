# ✦ Planeamos tus Sueños — Backend

API REST para el sitio web de organización de eventos en el Oriente Antioqueño, Colombia.

## Stack tecnológico

- **Framework:** Django 5 + Django REST Framework
- **Lenguaje:** Python 3
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación:** Django Admin

## Endpoints de la API

| Ruta | Descripción |
|---|---|
| `/api/catalogo/productos/` | Productos de alquiler |
| `/api/catalogo/servicios/` | Servicios de personal |
| `/api/portafolio/eventos/` | Eventos del portafolio |
| `/api/contacto/mensajes/` | Mensajes de contacto |
| `/api/contacto/cotizaciones/` | Cotizaciones de eventos |
| `/api/reservas/reservas/` | Reservas con anticipo |

## Instalación

```bash
git clone https://github.com/HarrisonORM/planeamos-tus-suenos-backend.git
cd planeamos-tus-suenos-backend
python -m venv entorno
entorno\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000

## Repositorio del frontend

[planeamos-tus-suenos-frontend](https://github.com/TU_USUARIO/planeamos-tus-suenos-frontend)