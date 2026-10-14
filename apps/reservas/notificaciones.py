import logging
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _pesos(valor):
    return "$" + f"{valor:,}".replace(",", ".")


def construir_mensaje(reserva):
    lineas = [
        "NUEVA SOLICITUD DE RESERVA",
        f"Cliente: {reserva.nombre_cliente}",
        f"Teléfono: {reserva.telefono}",
        f"Correo: {reserva.correo}",
        f"Fecha del evento: {reserva.fecha_evento.isoformat()}",
        f"Tipo: {reserva.get_tipo_reserva_display()}",
    ]
    if reserva.direccion:
        lineas.append(f"Dirección: {reserva.direccion}")
    lineas.append("")
    lineas.append("Detalle:")
    for item in reserva.detalle:
        lineas.append(
            f"- {item['nombre']} x{item['cantidad']} "
            f"({_pesos(item['subtotal'])})"
        )
    lineas.append("")
    lineas.append(f"Total estimado: {_pesos(reserva.valor_total)}")
    if reserva.descripcion:
        lineas.append(f"Notas del cliente: {reserva.descripcion}")
    lineas.append(f"Reserva #{reserva.pk}")
    return "\n".join(lineas)


def _enviar(mensaje):
    token = settings.TELEGRAM_BOT_TOKEN.strip()
    url = TELEGRAM_URL.format(token=token)
    datos = urlencode({
        "chat_id": settings.TELEGRAM_CHAT_ID.strip(),
        "text": mensaje,
    }).encode()
    try:
        with urlopen(url, data=datos, timeout=8) as r:
            logger.info("Telegram respondió %s", r.status)
    except HTTPError as error:
        logger.error(
            "Telegram rechazó el aviso (%s): %s",
            error.code,
            error.read().decode(errors="replace"),
        )
    except (URLError, OSError):
        logger.exception("No se pudo enviar el aviso de la reserva")


def notificar_nueva_reserva(reserva):
    """Envía los datos de la reserva por Telegram; nunca lanza errores."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.error("Telegram no configurado; no se notifica la reserva")
        return
    try:
        logger.info("Enviando aviso de la reserva #%s", reserva.pk)
        _enviar(construir_mensaje(reserva))
    except Exception:
        logger.exception("Falló el aviso de la reserva #%s", reserva.pk)
