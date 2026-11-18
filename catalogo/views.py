from django.contrib import messages
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
        formulario = EncargoForm(request.POST)
        if formulario.is_valid():
            encargo = formulario.save(commit=False)
            encargo.producto = producto
            encargo.save()
            messages.success(
                request,
                f'Tu encargo se registró correctamente. Código: {encargo.codigo}',
            )
            return redirect('catalogo:detalle_producto', pk=producto.pk)
    else:
        formulario = EncargoForm()

    return render(
        request,
        'catalogo/detalle_producto.html',
        {'producto': producto, 'formulario': formulario},
    )
