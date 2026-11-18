from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'),
]
