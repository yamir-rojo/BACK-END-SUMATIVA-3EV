from django.contrib import admin

from .models import Encargo, Linea, Producto


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'linea',
        'precio_en_pesos',
        'porciones',
        'apto_celiacos',
        'stock',
        'disponible',
    )
    list_filter = ('linea', 'apto_celiacos', 'disponible')
    search_fields = ('nombre',)

    @admin.display(description='Precio', ordering='precio')
    def precio_en_pesos(self, producto):
        return f'${producto.precio:,}'.replace(',', '.')


@admin.register(Encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'producto',
        'nombre_cliente',
        'correo_cliente',
        'fecha_retiro',
        'cantidad',
        'fecha_hora',
    )
    list_filter = ('producto', 'fecha_retiro')
    search_fields = ('nombre_cliente', 'correo_cliente')
    readonly_fields = ('codigo', 'fecha_hora')
