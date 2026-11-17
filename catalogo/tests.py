from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .admin import EncargoAdmin, ProductoAdmin
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


class CatalogoAdminTests(TestCase):
    def test_producto_muestra_precio_en_pesos_chilenos_y_permite_filtrar(self):
        linea = Linea.objects.create(nombre='Tortas')
        producto = Producto(
            nombre='Torta de chocolate',
            linea=linea,
            precio=18990,
            porciones=10,
        )
        admin_producto = ProductoAdmin(Producto, admin.site)

        self.assertEqual(admin_producto.precio_en_pesos(producto), '$18.990')
        self.assertEqual(admin_producto.list_filter[0][0], 'linea')
        self.assertIn('apto_celiacos', admin_producto.list_filter)
        self.assertIn('nombre', admin_producto.search_fields)

    def test_encargos_se_filtran_por_producto_y_fecha_de_retiro(self):
        admin_encargo = EncargoAdmin(Encargo, admin.site)

        self.assertEqual(admin_encargo.list_filter[0][0], 'producto')
        self.assertIn('fecha_retiro', admin_encargo.list_filter)
        self.assertIn('nombre_cliente', admin_encargo.search_fields)
        self.assertIn('correo_cliente', admin_encargo.search_fields)

    def test_filtro_por_producto_se_muestra_con_un_solo_producto(self):
        linea = Linea.objects.create(nombre='Tortas')
        Producto.objects.create(
            nombre='Torta de chocolate',
            linea=linea,
            fotografia='productos/torta.jpg',
            precio=18000,
            porciones=10,
        )
        superusuario = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(superusuario)
        response = self.client.get(reverse('admin:catalogo_encargo_changelist'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por producto')

    def test_filtro_por_linea_se_muestra_con_una_sola_linea(self):
        linea = Linea.objects.create(nombre='Tortas')
        Producto.objects.create(
            nombre='Torta de chocolate',
            linea=linea,
            fotografia='productos/torta.jpg',
            precio=18000,
            porciones=10,
        )
        superusuario = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(superusuario)
        response = self.client.get(reverse('admin:catalogo_producto_changelist'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por linea')

    def test_grupo_cocina_tiene_permisos_solicitados(self):
        grupo = Group.objects.get(name='Cocina')
        permisos = set(grupo.permissions.values_list('codename', flat=True))

        self.assertEqual(
            permisos,
            {
                'view_linea',
                'add_linea',
                'change_linea',
                'view_producto',
                'add_producto',
                'change_producto',
                'view_encargo',
            },
        )
