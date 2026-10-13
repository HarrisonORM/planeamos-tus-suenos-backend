from urllib.parse import urlencode
from uuid import uuid4
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
)
from rest_framework.response import Response
from .models import PagoReserva, Reserva
from .serializers import (
    ReservaSerializer,
    SolicitudReservaSerializer,
)
from .wompi import (
    generar_firma_integridad,
    verificar_firma_evento,
)


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        publicas = [
            "create",
            "fechas_ocupadas",
            "pago_anticipo",
            "estado_pago",
            "wompi_webhook",
        ]
        if self.action in publicas:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return SolicitudReservaSerializer
        return ReservaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get(
            "estado"
        )
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    @action(
        detail=False,
        methods=["get"],
        url_path="fechas-ocupadas",
    )
    def fechas_ocupadas(self, request):
        fechas = (
            Reserva.objects.filter(
                estado__in=[
                    "anticipo_pagado",
                    "confirmada",
                ],
                fecha_evento__gte=timezone.localdate(),
            )
            .values_list("fecha_evento", flat=True)
            .distinct()
            .order_by("fecha_evento")
        )
        return Response({
            "fechas_ocupadas": [
                fecha.isoformat() for fecha in fechas
            ]
        })

    @transaction.atomic
    @action(
        detail=False,
        methods=["post"],
        url_path="pago-anticipo",
    )
    def pago_anticipo(self, request):
        if not isinstance(request.data, dict):
            return Response(
                {"error": "Se esperaba un objeto JSON."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token_pago = (
                serializers.UUIDField().run_validation(
                    request.data.get("token_pago")
                )
            )
        except serializers.ValidationError as error:
            return Response(
                {"error": error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reserva = (
            Reserva.objects.select_for_update()
            .filter(token_pago=token_pago)
            .first()
        )
        if reserva is None:
            return Response(
                {"error": "No se encontró la reserva."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if reserva.estado != "pendiente":
            return Response(
                {"error": "La reserva no está pendiente."},
                status=status.HTTP_409_CONFLICT,
            )
        if not reserva.anticipo_validado:
            return Response(
                {
                    "error":
                        "El anticipo aún no fue validado."
                },
                status=status.HTTP_409_CONFLICT,
            )
        if reserva.valor_anticipo <= 0:
            return Response(
                {
                    "error":
                        "El anticipo debe ser positivo."
                },
                status=status.HTTP_409_CONFLICT,
            )
        if (
            reserva.valor_anticipo
            > reserva.valor_total
        ):
            return Response(
                {
                    "error":
                        (
                            "El anticipo supera "
                            "el valor total."
                        )
                },
                status=status.HTTP_409_CONFLICT,
            )

        llave_publica = settings.WOMPI_PUBLIC_KEY
        secreto_integridad = (
            settings.WOMPI_INTEGRITY_SECRET
        )
        secreto_eventos = settings.WOMPI_EVENTS_SECRET
        if not llave_publica:
            return self._wompi_no_configurado()
        if not secreto_integridad or not secreto_eventos:
            return self._wompi_no_configurado()
        if not llave_publica.startswith("pub_test_"):
            return Response(
                {
                    "error":
                        "Solo se permiten llaves Sandbox."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        pago = (
            PagoReserva.objects.select_for_update()
            .filter(reserva=reserva, estado="pendiente")
            .order_by("-creado")
            .first()
        )
        if (
            pago
            and pago.valor_anticipo
            != reserva.valor_anticipo
        ):
            return Response(
                {
                    "error":
                        (
                            "Hay un pago pendiente con "
                            "otro monto."
                        ),
                },
                status=status.HTTP_409_CONFLICT,
            )
        if pago is None:
            pago = PagoReserva.objects.create(
                reserva=reserva,
                referencia=(
                    f"RES-{reserva.pk}-{uuid4().hex}"
                ),
                valor_anticipo=reserva.valor_anticipo,
            )

        monto_centavos = pago.valor_anticipo * 100
        firma = generar_firma_integridad(
            pago.referencia,
            monto_centavos,
            "COP",
            secreto_integridad,
        )
        parametros = {
            "public-key": llave_publica,
            "currency": "COP",
            "amount-in-cents": monto_centavos,
            "reference": pago.referencia,
            "signature:integrity": firma,
            "customer-data:email": reserva.correo,
            "customer-data:full-name":
                reserva.nombre_cliente,
            "redirect-url": (
                settings.FRONTEND_URL.rstrip("/")
                + "/reserva/estado?referencia="
                + pago.referencia
            ),
        }
        url = (
            "https://checkout.wompi.co/p/?"
            + urlencode(parametros)
        )
        return Response({
            "checkout_url": url,
            "referencia": pago.referencia,
        })

    @action(
        detail=False,
        methods=["get"],
        url_path="estado-pago",
    )
    def estado_pago(self, request):
        referencia = request.query_params.get(
            "referencia",
            "",
        ).strip()
        if not referencia:
            return Response(
                {"error": "La referencia es obligatoria."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pago = (
            PagoReserva.objects
            .select_related("reserva")
            .filter(referencia=referencia)
            .first()
        )
        if pago is None:
            return Response(
                {"error": "No se encontró el pago."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({
            "referencia": pago.referencia,
            "estado_pago": pago.estado,
            "estado_reserva": pago.reserva.estado,
            "valor_anticipo": pago.valor_anticipo,
        })

    @transaction.atomic
    @action(
        detail=False,
        methods=["post"],
        url_path="wompi-webhook",
    )
    def wompi_webhook(self, request):
        secreto = settings.WOMPI_EVENTS_SECRET
        if not secreto:
            return self._wompi_no_configurado()
        if not isinstance(request.data, dict):
            return Response(
                {
                    "error":
                        (
                            "El evento debe ser "
                            "un objeto JSON."
                        )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not verificar_firma_evento(
            request.data,
            secreto,
        ):
            return Response(
                {"error": "Firma de evento no válida."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            request.data.get("event")
            != "transaction.updated"
        ):
            return Response({"estado": "ignorado"})

        datos = request.data.get("data")
        if not isinstance(datos, dict):
            return Response(
                {"error": "Datos del evento no válidos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        transaccion = datos.get("transaction")
        if not isinstance(transaccion, dict):
            return Response(
                {
                    "error":
                        "Faltan datos de la transacción."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        referencia = transaccion.get("reference")
        transaccion_id = transaccion.get("id")
        estado_wompi = transaccion.get("status")
        monto = transaccion.get("amount_in_cents")
        moneda = transaccion.get("currency")
        if not isinstance(referencia, str):
            return Response(
                {"error": "Referencia de pago no válida."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(transaccion_id, str):
            return Response(
                {"error": "ID de transacción inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(monto, bool) or not isinstance(
            monto,
            int,
        ):
            return Response(
                {
                    "error":
                        "Monto de transacción no válido."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if moneda != "COP":
            return Response(
                {
                    "error":
                        "Moneda de transacción no válida."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        estados = {
            "PENDING": "pendiente",
            "APPROVED": "aprobado",
            "DECLINED": "rechazado",
            "VOIDED": "anulado",
            "ERROR": "error",
        }
        if not isinstance(estado_wompi, str):
            return Response(
                {"error": "Estado de pago no válido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        estado_pago = estados.get(estado_wompi)
        if estado_pago is None:
            return Response(
                {"error": "Estado de pago no reconocido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pago = (
            PagoReserva.objects.select_for_update()
            .select_related("reserva")
            .filter(referencia=referencia)
            .first()
        )
        if pago is None:
            return Response(
                {
                    "error":
                        "Referencia de pago desconocida."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if monto != pago.valor_anticipo * 100:
            return Response(
                {"error": "El monto no coincide."},
                status=status.HTTP_409_CONFLICT,
            )
        if pago.estado == "aprobado":
            if pago.transaccion_id != transaccion_id:
                return Response(
                    {
                        "error":
                            "Pago duplicado no permitido."
                    },
                    status=status.HTTP_409_CONFLICT,
                )
            return Response({"estado": "procesado"})

        pago.estado = estado_pago
        pago.transaccion_id = transaccion_id
        pago.save(
            update_fields=[
                "estado",
                "transaccion_id",
                "actualizado",
            ]
        )
        if (
            estado_pago == "aprobado"
            and pago.reserva.estado == "pendiente"
        ):
            pago.reserva.estado = "anticipo_pagado"
            pago.reserva.save(
                update_fields=["estado", "actualizado"]
            )
        return Response({"estado": "procesado"})

    def _wompi_no_configurado(self):
        return Response(
            {"error": "Faltan variables de Wompi."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )