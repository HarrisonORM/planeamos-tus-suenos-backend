import logging
import threading
from urllib.error import URLError
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
    url = TELEGRAM_URL.format(token=settings.TELEGRAM_BOT_TOKEN)
    datos = urlencode({
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": mensaje,
    }).encode()
    try:
        with urlopen(url, data=datos, timeout=15) as r:
            if r.status != 200:
                logger.warning("Telegram respondió %s", r.status)
    except (URLError, OSError):
        logger.exception("No se pudo enviar el aviso de la reserva")


def notificar_nueva_reserva(reserva):
    """Envía los datos de la reserva por Telegram sin bloquear."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram no configurado; no se notifica la reserva")
        return
    mensaje = construir_mensaje(reserva)
    threading.Thread(target=_enviar, args=(mensaje,), daemon=True).start()
