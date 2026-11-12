import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Linea(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'línea'
        verbose_name_plural = 'líneas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    linea = models.ForeignKey(
        Linea,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    fotografia = models.FileField(upload_to='productos/')
    precio = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    porciones = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    apto_celiacos = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Encargo(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='encargos',
    )
    nombre_cliente = models.CharField(max_length=150)
    correo_cliente = models.EmailField()
    fecha_retiro = models.DateField()
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        verbose_name = 'encargo'
        verbose_name_plural = 'encargos'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f'{self.codigo} - {self.producto.nombre}'
