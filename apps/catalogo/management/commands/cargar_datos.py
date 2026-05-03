from django.core.management.base import BaseCommand
from apps.catalogo.models import (
    ProductoAlquiler,
    ServicioPersonal,
)
from apps.portafolio.models import EventoPortafolio

IMG = "https://images.unsplash.com/photo-"


class Command(BaseCommand):
    help = "Carga datos de ejemplo"

    def handle(self, *args, **options):
        self.stdout.write("Cargando datos...")

        # Crear superusuario si no existe
        from django.contrib.auth.models import User
        from decouple import config
        admin_pass = config(
            "ADMINISTRACION_PASSWORD",
            default="admin123"
        )
        if not User.objects.filter(
            username="administracion"
        ).exists():
            User.objects.create_superuser(
                username="administracion",
                email="harryson02@outlook.com",
                password=admin_pass
            )
            self.stdout.write(
                "  Superusuario 'administracion' creado"
            )

        # Limpiar datos existentes
        ProductoAlquiler.objects.all().delete()
        ServicioPersonal.objects.all().delete()
        EventoPortafolio.objects.all().delete()

        # Productos de alquiler
        productos = [
            {
                "nombre": "Silla Tiffany Dorada",
                "descripcion":
                    "Silla elegante en color dorado. "
                    + "Asiento acolchado incluido.",
                "categoria": "mobiliario",
                "precio": 5500,
                "unidad": "por día",
                "imagen":
                    IMG + "1555041469-a586c61ea9bc?w=600",
                "tipos_evento":
                    ["boda", "quinceañera", "corporativo"],
            },
            {
                "nombre": "Mesa Redonda para 8",
                "descripcion":
                    "Mesa redonda de 1.50m con "
                    + "mantelería blanca incluida.",
                "categoria": "mobiliario",
                "precio": 28000,
                "unidad": "por día",
                "imagen":
                    IMG + "1519167758481-83f550bb49b3?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo", "fiesta"],
            },
            {
                "nombre": "Silla Crossback Madera",
                "descripcion":
                    "Silla rústica en madera natural "
                    + "para eventos al aire libre.",
                "categoria": "mobiliario",
                "precio": 6500,
                "unidad": "por día",
                "imagen":
                    IMG + "1555041469-a586c61ea9bc?w=600",
                "tipos_evento": ["boda", "fiesta"],
            },
            {
                "nombre": "Copa de Vino Cristal",
                "descripcion":
                    "Copa de cristal para vino tinto. "
                    + "Capacidad 300ml.",
                "categoria": "menaje",
                "precio": 1800,
                "unidad": "por día",
                "imagen":
                    IMG + "1510812431401-41d2bd2722f3?w=600",
                "tipos_evento":
                    ["boda", "quinceañera", "corporativo"],
            },
            {
                "nombre": "Copa de Champaña Flauta",
                "descripcion":
                    "Copa alargada de cristal para "
                    + "champaña y vino espumoso.",
                "categoria": "menaje",
                "precio": 2000,
                "unidad": "por día",
                "imagen":
                    IMG + "1510812431401-41d2bd2722f3?w=600",
                "tipos_evento":
                    ["boda", "quinceañera", "corporativo"],
            },
            {
                "nombre": "Set de Cubertería Dorada",
                "descripcion":
                    "Juego completo: tenedor, cuchillo "
                    + "y cuchara. Acabado dorado.",
                "categoria": "menaje",
                "precio": 3500,
                "unidad": "por día",
                "imagen":
                    IMG + "1514362545857-3bc16c4c7d1b?w=600",
                "tipos_evento":
                    ["boda", "quinceañera"],
            },
            {
                "nombre": "Vajilla Porcelana Blanca",
                "descripcion":
                    "Set de tres piezas: plato base, "
                    + "principal y postre.",
                "categoria": "menaje",
                "precio": 4200,
                "unidad": "por día",
                "imagen":
                    IMG + "1514362545857-3bc16c4c7d1b?w=600",
                "tipos_evento":
                    ["boda", "quinceañera", "corporativo"],
            },
            {
                "nombre": "Equipo de Sonido Profesional",
                "descripcion":
                    "2 bafles 1000W, mesa de mezcla "
                    + "y 2 micrófonos inalámbricos.",
                "categoria": "sonido",
                "precio": 350000,
                "unidad": "por día",
                "imagen":
                    IMG + "1505236858219-8359eb29e329?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo", "fiesta"],
            },
            {
                "nombre": "Candelabro Dorado de Mesa",
                "descripcion":
                    "Candelabro elegante de 5 velas. "
                    + "Altura 45cm. Velas incluidas.",
                "categoria": "iluminacion",
                "precio": 22000,
                "unidad": "por día",
                "imagen":
                    IMG + "1478146059778-26028b07395a?w=600",
                "tipos_evento":
                    ["boda", "quinceañera"],
            },
            {
                "nombre": "Candelabro de Piso Clásico",
                "descripcion":
                    "Candelabro alto de piso, 1.20m. "
                    + "Aspecto señorial.",
                "categoria": "iluminacion",
                "precio": 45000,
                "unidad": "por día",
                "imagen":
                    IMG + "1478146059778-26028b07395a?w=600",
                "tipos_evento": ["boda"],
            },
            {
                "nombre": "Luces LED de Colores",
                "descripcion":
                    "Set de 10 luces LED ambientales "
                    + "con control remoto.",
                "categoria": "iluminacion",
                "precio": 85000,
                "unidad": "por día",
                "imagen":
                    IMG + "1505236858219-8359eb29e329?w=600",
                "tipos_evento":
                    ["quinceañera", "fiesta",
                     "corporativo"],
            },
            {
                "nombre": "Arco Floral para Ceremonia",
                "descripcion":
                    "Estructura metálica dorada 2.5m "
                    + "con adorno floral.",
                "categoria": "decoracion",
                "precio": 180000,
                "unidad": "por día",
                "imagen":
                    IMG + "1487530811176-3780de880c2d?w=600",
                "tipos_evento": ["boda"],
            },
        ]

        for p in productos:
            ProductoAlquiler.objects.create(**p)
        self.stdout.write(
            f"  {len(productos)} productos creados"
        )

        # Servicios de personal
        servicios = [
            {
                "nombre": "Mesero Profesional",
                "descripcion":
                    "Personal uniformado con "
                    + "experiencia en eventos formales.",
                "categoria": "meseros",
                "precio": 180000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1414235077428-338989a2e8c0?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo", "fiesta"],
            },
            {
                "nombre":
                    "Chef Especializado en Bodas",
                "descripcion":
                    "Chef con 10+ años. Menú "
                    + "personalizado hasta 300.",
                "categoria": "chef",
                "precio": 1800000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1577219491135-ce391730fb2c?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo"],
            },
            {
                "nombre":
                    "Chef Parrilla & Estaciones",
                "descripcion":
                    "Especialista en asado en vivo "
                    + "y parrilla argentina.",
                "categoria": "chef",
                "precio": 1200000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1577219491135-ce391730fb2c?w=600",
                "tipos_evento":
                    ["fiesta", "corporativo"],
            },
            {
                "nombre": "DJ Profesional + Equipo",
                "descripcion":
                    "DJ con equipo completo, luces "
                    + "y animación.",
                "categoria": "dj",
                "precio": 850000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1571266028243-d220c6a1b0e4?w=600",
                "tipos_evento":
                    ["boda", "quinceañera", "fiesta"],
            },
            {
                "nombre": "Mesa de Postres Gourmet",
                "descripcion":
                    "Mesa decorada con postres "
                    + "artesanales para 100 personas.",
                "categoria": "reposteria",
                "precio": 650000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1535254973040-607b474cb50d?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo"],
            },
            {
                "nombre": "Torta Personalizada",
                "descripcion":
                    "Torta de 3 a 5 pisos, sabores "
                    + "a elección.",
                "categoria": "reposteria",
                "precio": 480000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1535254973040-607b474cb50d?w=600",
                "tipos_evento":
                    ["boda", "quinceañera"],
            },
            {
                "nombre": "Fotografía Profesional",
                "descripcion":
                    "8 horas, 500+ fotos editadas "
                    + "entregadas en 15 días.",
                "categoria": "fotografia",
                "precio": 1600000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1606216794074-735e91aa2c92?w=600",
                "tipos_evento":
                    ["boda", "quinceañera",
                     "corporativo", "fiesta"],
            },
            {
                "nombre":
                    "Decoración Floral Completa",
                "descripcion":
                    "Ambientación floral integral: "
                    + "mesa principal, centros y entrada.",
                "categoria": "floreria",
                "precio": 2200000,
                "unidad": "por evento",
                "imagen":
                    IMG + "1487530811176-3780de880c2d?w=600",
                "tipos_evento":
                    ["boda", "quinceañera"],
            },
        ]

        for s in servicios:
            ServicioPersonal.objects.create(**s)
        self.stdout.write(
            f"  {len(servicios)} servicios creados"
        )

        # Portafolio
        eventos = [
            {
                "titulo": "Boda María & Juan",
                "descripcion":
                    "Ceremonia al aire libre "
                    + "en hacienda tradicional",
                "tipo_evento": "boda",
                "imagen":
                    IMG + "1519741497674-611481863552?w=800",
                "fecha": "2024-11-15",
                "lugar":
                    "Hacienda El Paraíso, Guarne",
            },
            {
                "titulo": "Quinceañera Isabella",
                "descripcion":
                    "Celebración estilo princesa "
                    + "con ambientación dorada",
                "tipo_evento": "quinceañera",
                "imagen":
                    IMG + "1464366400600-7168b8af9bc3?w=800",
                "fecha": "2024-10-20",
                "lugar":
                    "Salón Los Rosales, Rionegro",
            },
            {
                "titulo": "Boda Sofía & Andrés",
                "descripcion":
                    "Boda íntima con 80 invitados "
                    + "en jardín privado",
                "tipo_evento": "boda",
                "imagen":
                    IMG + "1511795409834-ef04bbd61622?w=800",
                "fecha": "2024-09-07",
                "lugar": "Llanogrande, Rionegro",
            },
            {
                "titulo": "Quinceañera Valentina",
                "descripcion":
                    "Fiesta temática con show "
                    + "de luces y coreografía",
                "tipo_evento": "quinceañera",
                "imagen":
                    IMG + "1478146896981-b80fe463b330?w=800",
                "fecha": "2024-08-12",
                "lugar":
                    "Hacienda La Pradera, La Ceja",
            },
            {
                "titulo":
                    "Evento Corporativo GrupoX",
                "descripcion":
                    "Evento de fin de año "
                    + "con 200 asistentes",
                "tipo_evento": "corporativo",
                "imagen":
                    IMG + "1511578314322-379afb476865?w=800",
                "fecha": "2024-12-18",
                "lugar": "Rionegro",
            },
            {
                "titulo": "Boda Laura & Carlos",
                "descripcion":
                    "Boda campestre con detalles "
                    + "rústicos y florales",
                "tipo_evento": "boda",
                "imagen":
                    IMG + "1465495976277-4387d4b0b4c6?w=800",
                "fecha": "2024-07-22",
                "lugar":
                    "Finca Los Olivos, Marinilla",
            },
            {
                "titulo":
                    "Cumpleaños 40 — Patricia",
                "descripcion":
                    "Fiesta temática años 80 "
                    + "con show en vivo",
                "tipo_evento": "fiesta",
                "imagen":
                    IMG + "1530103862676-de8c9debad1d?w=800",
                "fecha": "2024-06-15",
                "lugar": "Llanogrande",
            },
            {
                "titulo": "Boda Camila & David",
                "descripcion":
                    "Ceremonia religiosa + "
                    + "recepción de gala para 250",
                "tipo_evento": "boda",
                "imagen":
                    IMG + "1519225421980-715cb0215aed?w=800",
                "fecha": "2024-05-11",
                "lugar": "Rionegro",
            },
        ]

        for e in eventos:
            EventoPortafolio.objects.create(**e)
        self.stdout.write(
            f"  {len(eventos)} eventos creados"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Datos cargados exitosamente"
            )
        )