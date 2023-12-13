from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_admin),
    path('registrar_producto/', views.registrar_producto),
    path('edicion_producto/<idProd>', views.edicion_producto, name = 'edicion_producto'),
    path('editar_producto/', views.editar_producto),
    path('eliminar_producto/<idProd>', views.eliminar_producto, name = 'eliminar_producto'),

    path('gestion_clientes/', views.gestion_clientes, name = 'gestion_clientes'),
    path('registrar_cliente/', views.registrar_cliente),
    path('edicion_cliente/<rut>', views.edicion_cliente, name = 'edicion_cliente'),
    path('editar_cliente/', views.editar_cliente, name = 'editar_cliente'),
    path('eliminar_cliente/<rut>', views.eliminar_cliente, name = 'eliminar_cliente'),

]