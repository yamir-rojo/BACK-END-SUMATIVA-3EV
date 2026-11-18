from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EncargoForm
from .models import Linea, Producto


def inicio(request):
    productos = Producto.objects.filter(disponible=True).select_related('linea')
    busqueda = request.GET.get('q', '').strip()
    linea_id = request.GET.get('linea', '').strip()
    linea_seleccionada = None

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if linea_id:
        if linea_id.isdecimal():
            linea_seleccionada = int(linea_id)
            productos = productos.filter(linea_id=linea_seleccionada)
        else:
            productos = productos.none()

    return render(
        request,
        'catalogo/inicio.html',
        {
            'productos': productos,
            'lineas': Linea.objects.all(),
            'busqueda': busqueda,
            'linea_seleccionada': linea_seleccionada,
        },
    )


def detalle_producto(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related('linea'),
        pk=pk,
        disponible=True,
    )
    if request.method == 'POST':
        formulario = EncargoForm(request.POST, producto=producto)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad']
            with transaction.atomic():
                stock_descontado = Producto.objects.filter(
                    pk=producto.pk,
                    disponible=True,
                    stock__gte=cantidad,
                ).update(stock=F('stock') - cantidad)
                if stock_descontado:
                    encargo = formulario.save(commit=False)
                    encargo.producto = producto
                    encargo.save()

            if stock_descontado:
                messages.success(
                    request,
                    f'Tu encargo se registró correctamente. Código: {encargo.codigo}',
                )
                return redirect('catalogo:detalle_producto', pk=producto.pk)

            producto = get_object_or_404(
                Producto.objects.select_related('linea'),
                pk=producto.pk,
                disponible=True,
            )
            formulario.add_error(
                'cantidad',
                f'Solo hay {producto.stock} unidades disponibles.',
            )
    else:
        formulario = EncargoForm(producto=producto)

    return render(
        request,
        'catalogo/detalle_producto.html',
        {'producto': producto, 'formulario': formulario},
    )
