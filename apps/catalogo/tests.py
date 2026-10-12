from django.test import TestCase
from rest_framework.test import APIClient
from .models import Locacion, Paquete


class PaqueteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Paquete.objects.create(
            nombre="Paquete boda",
            descripcion="Paquete para bodas",
            tipo_evento="boda",
            precio_desde=1000000,
            precio_hasta=2000000,
        )
        Paquete.objects.create(
            nombre="Paquete fiesta",
            descripcion="Paquete para fiestas",
            tipo_evento="fiesta",
            precio_desde=500000,
            precio_hasta=1000000,
        )

    def test_lista_paquetes(self):
        respuesta = self.client.get(
            "/api/catalogo/paquetes/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["count"], 2)

    def test_filtra_paquetes_por_tipo_evento(self):
        respuesta = self.client.get(
            "/api/catalogo/paquetes/",
            {"tipo_evento": "boda"},
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["count"], 1)
        self.assertEqual(
            respuesta.data["results"][0]["nombre"],
            "Paquete boda",
        )


class LocacionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Locacion.objects.create(
            nombre="Finca Oriente",
            descripcion="Finca para eventos",
            municipio="Rionegro",
            capacidad=100,
        )
        Locacion.objects.create(
            nombre="Salón Ceja",
            descripcion="Salón de eventos",
            municipio="La Ceja",
            capacidad=80,
        )

    def test_lista_locaciones(self):
        respuesta = self.client.get(
            "/api/catalogo/locaciones/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["count"], 2)

    def test_filtra_locaciones_por_municipio(self):
        respuesta = self.client.get(
            "/api/catalogo/locaciones/",
            {"municipio": "rionegro"},
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["count"], 1)
        self.assertEqual(
            respuesta.data["results"][0]["nombre"],
            "Finca Oriente",
        )
