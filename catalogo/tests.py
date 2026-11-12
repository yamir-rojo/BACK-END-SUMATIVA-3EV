from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Encargo, Linea, Producto


class CatalogoModelsTests(TestCase):
    def setUp(self):
        self.linea = Linea.objects.create(nombre='Tortas')
        self.producto = Producto.objects.create(
            nombre='Torta de chocolate',
            linea=self.linea,
            fotografia='productos/torta.jpg',
            precio=18000,
            porciones=10,
            apto_celiacos=False,
            stock=3,
            disponible=True,
        )

    def test_linea_nombre_es_unico(self):
        self.assertEqual(str(self.linea), 'Tortas')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Linea.objects.create(nombre='Tortas')

    def test_encargo_genera_codigo_y_se_elimina_con_producto(self):
        encargo = Encargo.objects.create(
            producto=self.producto,
            nombre_cliente='Ana Pérez',
            correo_cliente='ana@example.com',
            fecha_retiro='2026-11-20',
            cantidad=1,
        )

        self.assertIsNotNone(encargo.codigo)
        self.assertIn('Torta de chocolate', str(encargo))
        self.producto.delete()

        self.assertFalse(Encargo.objects.filter(pk=encargo.pk).exists())

    def test_productos_y_encargos_se_eliminan_con_linea(self):
        encargo = Encargo.objects.create(
            producto=self.producto,
            nombre_cliente='Ana Pérez',
            correo_cliente='ana@example.com',
            fecha_retiro='2026-11-20',
            cantidad=1,
        )

        self.linea.delete()

        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
        self.assertFalse(Encargo.objects.filter(pk=encargo.pk).exists())
