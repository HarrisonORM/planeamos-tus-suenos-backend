# CLAUDE.md — Backend Context

## Proyecto
API REST para "Planeamos tus Sueños", empresa de eventos del Oriente Antioqueño.
Backend del proyecto. El frontend está en un repositorio separado.

## Stack
- Django 5 + Django REST Framework
- Python 3
- SQLite (desarrollo) / PostgreSQL Supabase (producción)
- django-cors-headers para permitir conexión del frontend
- python-decouple para variables de entorno

## Apps
- apps.catalogo → ProductoAlquiler, ServicioPersonal
- apps.portafolio → EventoPortafolio
- apps.contacto → MensajeContacto, Cotizacion
- apps.reservas → Reserva

## API Endpoints
- GET /api/catalogo/productos/?categoria=
- GET /api/catalogo/servicios/?categoria=
- GET /api/portafolio/eventos/?tipo_evento=
- POST /api/contacto/mensajes/
- POST /api/contacto/cotizaciones/
- GET/POST /api/reservas/reservas/?estado=

## Comandos Útiles
- python manage.py runserver → levantar servidor
- python manage.py cargar_datos → cargar datos de ejemplo
- python manage.py makemigrations → crear migraciones
- python manage.py migrate → aplicar migraciones
- python manage.py createsuperuser → crear admin

## CORS
Permite conexiones desde http://localhost:3000 (frontend en desarrollo)

## Pendiente
- Modelos para Paquete y Locacion (opcional)
- Integración Wompi para pagos
- Envío de correos de confirmación
- Despliegue en Railway con PostgreSQL
