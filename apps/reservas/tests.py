import hashlib
from urllib.parse import parse_qs, urlparse
from django.test import TestCase
from django.test import SimpleTestCase
from django.test import override_settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from apps.catalogo.models import (
    ProductoAlquiler,
    ServicioPersonal,
)
from .models import PagoReserva, Reserva
from .wompi import (
    generar_firma_integridad,
    verificar_firma_evento,
)


class FechasOcupadasApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def crear_reserva(self, estado, fecha_evento):
        return Reserva.objects.create(
            nombre_cliente="Cliente de prueba",
            telefono="3001234567",
            correo="cliente@example.com",
            tipo_reserva="evento",
            fecha_evento=fecha_evento,
            estado=estado,
        )

    def test_devuelve_fechas_ocupadas_unicas(self):
        hoy = timezone.localdate()
        fecha_confirmada = hoy + timedelta(days=10)
        fecha_pendiente = hoy + timedelta(days=11)

        self.crear_reserva(
            "anticipo_pagado",
            fecha_confirmada,
        )
        self.crear_reserva(
            "confirmada",
            fecha_confirmada,
        )
        self.crear_reserva(
            "pendiente",
            fecha_pendiente,
        )
        self.crear_reserva(
            "cancelada",
            hoy + timedelta(days=12),
        )
        self.crear_reserva(
            "confirmada",
            hoy - timedelta(days=1),
        )

        respuesta = self.client.get(
            "/api/reservas/reservas/fechas-ocupadas/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.data["fechas_ocupadas"],
            [fecha_confirmada.isoformat()],
        )

    def test_devuelve_lista_vacia_sin_reservas(self):
        respuesta = self.client.get(
            "/api/reservas/reservas/fechas-ocupadas/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.data["fechas_ocupadas"],
            [],
        )


class CrearSolicitudReservaApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producto = ProductoAlquiler.objects.create(
            nombre="Silla",
            descripcion="Silla para eventos",
            categoria="mobiliario",
            precio=25000,
        )
        self.servicio = ServicioPersonal.objects.create(
            nombre="Mesero",
            descripcion="Servicio de mesero",
            categoria="meseros",
            precio=100000,
        )

    def crear_solicitud(self, fecha_evento, **extra):
        datos = {
            "nombre_cliente": "Cliente de prueba",
            "telefono": "3001234567",
            "correo": "cliente@example.com",
            "fecha_evento": fecha_evento.isoformat(),
            "items": [
                {
                    "id": self.producto.pk,
                    "tipo": "producto",
                    "cantidad": 4,
                }
            ],
            **extra,
        }
        return self.client.post(
            "/api/reservas/reservas/",
            datos,
            format="json",
        )

    def test_calcula_total_con_precio_oficial_y_ignora_montos_cliente(self):
        fecha_evento = (
            timezone.localdate() + timedelta(days=20)
        )
        respuesta = self.crear_solicitud(
            fecha_evento,
            valor_total=1500000,
            valor_anticipo=300000,
            estado="confirmada",
            notas="Nota interna no autorizada",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_201_CREATED,
        )
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.estado, "pendiente")
        self.assertEqual(reserva.notas, "")
        self.assertEqual(reserva.tipo_reserva, "alquiler")
        self.assertEqual(reserva.valor_total, 100000)
        self.assertEqual(reserva.valor_anticipo, 0)
        self.assertEqual(reserva.detalle[0]["precio_unitario"], 25000)
        self.assertEqual(respuesta.data["valor_total"], 100000)

    def test_notifica_por_whatsapp_al_crear_la_reserva(self):
        from unittest.mock import patch
        fecha_evento = timezone.localdate() + timedelta(days=22)
        with patch(
            "apps.reservas.views.notificar_nueva_reserva"
        ) as notificar, self.captureOnCommitCallbacks(execute=True):
            respuesta = self.crear_solicitud(fecha_evento)

        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        notificar.assert_called_once_with(Reserva.objects.get())

    def test_mensaje_whatsapp_incluye_datos_de_la_reserva(self):
        from .notificaciones import construir_mensaje
        fecha_evento = timezone.localdate() + timedelta(days=23)
        self.crear_solicitud(fecha_evento)
        mensaje = construir_mensaje(Reserva.objects.get())

        self.assertIn("Cliente de prueba", mensaje)
        self.assertIn("3001234567", mensaje)
        self.assertIn("Silla x4", mensaje)
        self.assertIn("$100.000", mensaje)

    def test_calcula_total_de_productos_y_servicios(self):
        fecha_evento = (
            timezone.localdate() + timedelta(days=21)
        )
        respuesta = self.crear_solicitud(
            fecha_evento,
            items=[
                {
                    "id": self.producto.pk,
                    "tipo": "producto",
                    "cantidad": 2,
                },
                {
                    "id": self.servicio.pk,
                    "tipo": "servicio",
                    "cantidad": 1,
                },
            ],
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_201_CREATED,
        )
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.tipo_reserva, "evento")
        self.assertEqual(reserva.valor_total, 150000)
        self.assertEqual(len(reserva.detalle), 2)

    def test_rechaza_articulos_no_disponibles(self):
        self.producto.disponible = False
        self.producto.save(update_fields=["disponible"])

        respuesta = self.crear_solicitud(
            timezone.localdate() + timedelta(days=22)
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Reserva.objects.count(), 0)

    def test_rechaza_fecha_ocupada(self):
        fecha_evento = (
            timezone.localdate() + timedelta(days=23)
        )
        Reserva.objects.create(
            nombre_cliente="Reserva existente",
            telefono="3001234567",
            correo="existente@example.com",
            tipo_reserva="evento",
            fecha_evento=fecha_evento,
            estado="confirmada",
        )

        respuesta = self.crear_solicitud(fecha_evento)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Reserva.objects.count(), 1)

    def test_rechaza_fecha_pasada(self):
        respuesta = self.crear_solicitud(
            timezone.localdate() - timedelta(days=1)
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Reserva.objects.count(), 0)

    def test_rechaza_articulos_duplicados(self):
        fecha_evento = (
            timezone.localdate() + timedelta(days=24)
        )
        respuesta = self.crear_solicitud(
            fecha_evento,
            items=[
                {
                    "id": self.producto.pk,
                    "tipo": "producto",
                    "cantidad": 1,
                },
                {
                    "id": self.producto.pk,
                    "tipo": "producto",
                    "cantidad": 2,
                },
            ],
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Reserva.objects.count(), 0)

    def test_listado_publico_requiere_administrador(self):
        respuesta = self.client.get(
            "/api/reservas/reservas/"
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )


class FirmasWompiTests(SimpleTestCase):
    def test_genera_firma_de_integridad(self):
        secreto = "secreto-de-prueba"
        cadena = "ref-1" + "30000" + "COP" + secreto
        esperado = hashlib.sha256(
            cadena.encode("utf-8")
        ).hexdigest()

        firma = generar_firma_integridad(
            "ref-1",
            30000,
            "COP",
            secreto,
        )

        self.assertEqual(firma, esperado)

    def test_rechaza_evento_con_datos_alterados(self):
        secreto = "secreto-de-prueba"
        evento = {
            "data": {
                "transaction": {
                    "id": "transaccion-1",
                    "status": "APPROVED",
                    "amount_in_cents": 30000,
                },
            },
            "signature": {
                "properties": [
                    "transaction.id",
                    "transaction.status",
                    "transaction.amount_in_cents",
                ],
                "timestamp": 1700000000,
            },
        }
        cadena = (
            "transaccion-1APPROVED30000"
            "1700000000"
            + secreto
        )
        evento["signature"]["checksum"] = (
            hashlib.sha256(
                cadena.encode("utf-8")
            ).hexdigest()
        )
        self.assertTrue(
            verificar_firma_evento(evento, secreto)
        )

        evento["data"]["transaction"][
            "amount_in_cents"
        ] = 30001
        self.assertFalse(
            verificar_firma_evento(evento, secreto)
        )


@override_settings(
    WOMPI_PUBLIC_KEY="pub_test_prueba",
    WOMPI_INTEGRITY_SECRET="integridad-prueba",
    WOMPI_EVENTS_SECRET="eventos-prueba",
    FRONTEND_URL="https://frontend.example.com/",
)
class PagoWompiApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reserva = Reserva.objects.create(
            nombre_cliente="Cliente de prueba",
            telefono="3001234567",
            correo="cliente@example.com",
            tipo_reserva="evento",
            fecha_evento=(
                timezone.localdate() + timedelta(days=30)
            ),
            valor_total=1000000,
            valor_anticipo=300000,
            anticipo_validado=True,
        )

    def iniciar_pago(self, token=None):
        datos = {}
        if token is not None:
            datos["token_pago"] = str(token)
        return self.client.post(
            "/api/reservas/reservas/pago-anticipo/",
            datos,
            format="json",
        )

    def crear_evento(self, pago, monto=None):
        secreto = "eventos-prueba"
        transaccion = {
            "id": "transaccion-prueba",
            "reference": pago.referencia,
            "status": "APPROVED",
            "amount_in_cents": (
                pago.valor_anticipo * 100
                if monto is None
                else monto
            ),
            "currency": "COP",
        }
        propiedades = [
            "transaction.id",
            "transaction.reference",
            "transaction.status",
            "transaction.amount_in_cents",
            "transaction.currency",
        ]
        marca_tiempo = 1700000000
        valores = [
            transaccion[parte.split(".")[1]]
            for parte in propiedades
        ]
        cadena = (
            "".join(str(valor) for valor in valores)
            + str(marca_tiempo)
            + secreto
        )
        return {
            "event": "transaction.updated",
            "data": {"transaction": transaccion},
            "signature": {
                "properties": propiedades,
                "timestamp": marca_tiempo,
                "checksum": hashlib.sha256(
                    cadena.encode("utf-8")
                ).hexdigest(),
            },
        }

    def enviar_evento(self, evento):
        return self.client.post(
            "/api/reservas/reservas/wompi-webhook/",
            evento,
            format="json",
        )

    def test_checkout_requiere_token_pago(self):
        respuesta = self.iniciar_pago()

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_checkout_exige_anticipo_validado(self):
        self.reserva.anticipo_validado = False
        self.reserva.save(
            update_fields=["anticipo_validado"]
        )

        respuesta = self.iniciar_pago(
            self.reserva.token_pago
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_409_CONFLICT,
        )

    @override_settings(
        WOMPI_PUBLIC_KEY="",
        WOMPI_INTEGRITY_SECRET="",
        WOMPI_EVENTS_SECRET="",
    )
    def test_checkout_exige_configuracion_wompi(self):
        respuesta = self.iniciar_pago(
            self.reserva.token_pago
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    def test_checkout_firma_monto_y_reutiliza_referencia(
        self,
    ):
        primera = self.iniciar_pago(
            self.reserva.token_pago
        )
        segunda = self.iniciar_pago(
            self.reserva.token_pago
        )

        self.assertEqual(
            primera.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            segunda.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            primera.data["referencia"],
            segunda.data["referencia"],
        )
        self.assertEqual(PagoReserva.objects.count(), 1)

        consulta = parse_qs(
            urlparse(primera.data["checkout_url"]).query
        )
        self.assertEqual(
            consulta["amount-in-cents"],
            ["30000000"],
        )
        self.assertEqual(
            consulta["public-key"],
            ["pub_test_prueba"],
        )
        self.assertEqual(
            consulta["redirect-url"],
            [
                "https://frontend.example.com/"
                "reserva/estado?referencia="
                + primera.data["referencia"]
            ],
        )
        self.assertEqual(
            consulta["signature:integrity"],
            [
                generar_firma_integridad(
                    primera.data["referencia"],
                    30000000,
                    "COP",
                    "integridad-prueba",
                )
            ],
        )

    def test_estado_pago_es_publico_y_no_expone_datos_personales(
        self,
    ):
        pago = PagoReserva.objects.create(
            reserva=self.reserva,
            referencia="RES-ESTADO-1",
            valor_anticipo=300000,
        )

        respuesta = self.client.get(
            "/api/reservas/reservas/estado-pago/",
            {"referencia": pago.referencia},
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            respuesta.data,
            {
                "referencia": pago.referencia,
                "estado_pago": "pendiente",
                "estado_reserva": "pendiente",
                "valor_anticipo": 300000,
            },
        )
        self.assertNotIn("correo", respuesta.data)
        self.assertNotIn("nombre_cliente", respuesta.data)

    def test_estado_pago_exige_referencia(self):
        respuesta = self.client.get(
            "/api/reservas/reservas/estado-pago/"
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_estado_pago_no_revela_referencias_desconocidas(self):
        respuesta = self.client.get(
            "/api/reservas/reservas/estado-pago/",
            {"referencia": "no-existe"},
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_webhook_rechaza_firma_invalida(self):
        pago = PagoReserva.objects.create(
            reserva=self.reserva,
            referencia="reserva-firma-invalida",
            valor_anticipo=300000,
        )
        evento = self.crear_evento(pago)
        evento["data"]["transaction"][
            "amount_in_cents"
        ] = 30000001

        respuesta = self.enviar_evento(evento)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        pago.refresh_from_db()
        self.assertEqual(pago.estado, "pendiente")

    def test_webhook_rechaza_monto_distinto(self):
        pago = PagoReserva.objects.create(
            reserva=self.reserva,
            referencia="reserva-monto-distinto",
            valor_anticipo=300000,
        )
        evento = self.crear_evento(
            pago,
            monto=30000001,
        )

        respuesta = self.enviar_evento(evento)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_409_CONFLICT,
        )
        pago.refresh_from_db()
        self.assertEqual(pago.estado, "pendiente")

    def test_webhook_aprueba_pago_y_es_idempotente(self):
        pago = PagoReserva.objects.create(
            reserva=self.reserva,
            referencia="reserva-aprobada",
            valor_anticipo=300000,
        )
        evento = self.crear_evento(pago)

        primera = self.enviar_evento(evento)
        segunda = self.enviar_evento(evento)

        self.assertEqual(
            primera.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            segunda.status_code,
            status.HTTP_200_OK,
        )
        pago.refresh_from_db()
        self.reserva.refresh_from_db()
        self.assertEqual(pago.estado, "aprobado")
        self.assertEqual(
            self.reserva.estado,
            "anticipo_pagado",
        )
