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
| `/api/catalogo/paquetes/` | Paquetes de eventos |
| `/api/catalogo/locaciones/` | Locaciones |
| `/api/portafolio/eventos/` | Eventos del portafolio |
| `/api/contacto/mensajes/` | Mensajes de contacto |
| `/api/contacto/cotizaciones/` | Cotizaciones de eventos |
| `/api/reservas/reservas/` | Solicitudes de reserva |
| `/api/reservas/reservas/fechas-ocupadas/` | Fechas |

### Filtros y acceso

- Productos y servicios aceptan `?categoria=`.
- Eventos aceptan `?tipo_evento=`.
- Locaciones aceptan `?municipio=`.
- Las fechas ocupadas excluyen reservas pendientes
  y canceladas.
- Crear una reserva es público; consultar y administrar
  reservas requiere una cuenta de administrador.

### Solicitudes desde el cotizador

El cliente crea una solicitud en
`POST /api/reservas/reservas/` con sus datos, la fecha y
los artículos seleccionados. Cada artículo incluye el ID
del catálogo, el tipo (`producto` o `servicio`) y la
cantidad:

```json
{
  "nombre_cliente": "Nombre del cliente",
  "telefono": "3001234567",
  "correo": "cliente@example.com",
  "direccion": "Lugar del evento",
  "fecha_evento": "2027-06-15",
  "descripcion": "Detalles adicionales",
  "items": [
    {
      "id": 1,
      "tipo": "producto",
      "cantidad": 10
    }
  ]
}
```

El servidor verifica la disponibilidad de cada artículo y
calcula el total con los precios vigentes del catálogo;
no confía en montos enviados por el cliente. La respuesta
incluye el detalle y total calculados, y un `token_pago`.
El anticipo comienza en cero y un administrador debe
definirlo y validarlo antes de que el pago con Wompi quede
habilitado. La fecha se valida nuevamente al crear la
solicitud, además de consultarse con
`GET /api/reservas/reservas/fechas-ocupadas/`.

## Pagos con Wompi Sandbox

El flujo actual está limitado a Sandbox. No permite
procesar pagos reales.

1. El cliente crea una reserva con
   `POST /api/reservas/reservas/`.
2. La respuesta de creación incluye `token_pago`.
3. Un administrador revisa el valor del anticipo y activa
   `anticipo_validado` en el panel `/admin/`.
4. El cliente inicia el checkout:

```http
POST /api/reservas/reservas/pago-anticipo/
Content-Type: application/json
```

```json
{
  "token_pago": "UUID-recibido-al-crear-la-reserva"
}
```

La respuesta incluye `checkout_url` y `referencia`.
El cliente debe abrir `checkout_url` para pagar.
No compartas el token de pago con terceros.
Wompi redirige al cliente a
`FRONTEND_URL/reserva/estado?referencia=...`, donde se
consulta únicamente el estado del pago y de la reserva.
Configura `FRONTEND_URL` con el origen público del
frontend en producción.

Wompi envía el resultado a:

```text
POST /api/reservas/reservas/wompi-webhook/
```

Configura esta URL en Wompi para el evento
`transaction.updated`. El backend verifica el checksum
con el secreto de eventos antes de actualizar el pago.

Define estas variables en el entorno local o en Render:

- `WOMPI_PUBLIC_KEY`: llave pública `pub_test_`.
- `WOMPI_INTEGRITY_SECRET`: secreto de integridad.
- `WOMPI_EVENTS_SECRET`: secreto para firmar eventos.

Obtén las llaves de Sandbox desde el panel de Wompi.
No publiques sus valores en el repositorio.

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