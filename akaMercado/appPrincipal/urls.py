from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_admin),
    path('registrar_producto/', views.registrar_producto),
    path('edicion_producto/<idProd>', views.edicion_producto, name = 'edicion_producto'),
    path('editar_producto/', views.editar_producto),
    path('eliminar_producto/<idProd>', views.eliminar_producto, name = 'eliminar_producto')
]