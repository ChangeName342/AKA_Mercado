"""
URL configuration for akaMercado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from appPrincipal.views import (
    index, registro, nosotros, login_admin, login_cliente, cerrar_sesion, 
    vista_admin, vista_cliente, rotiseria, abarrotes, productos, agregar_producto,
    eliminar_producto, restar_producto, limpiar_carrito, carniceria, eliminar_productos,
    resumen_compra, confirmacion
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'home'),
    path('nosotros/', nosotros, name = 'nosotros'),
    path('registro/', registro, name = 'registro'),
    path('login_cliente/', login_cliente, name = 'login_cliente'),
    path('login_admin/', login_admin, name = 'login_admin'),
    path('cerrar_sesion/', cerrar_sesion, name = 'cerrar_sesion'),
    path('vista_cliente/', vista_cliente, name = 'vista_cliente'),
    path('vista_admin/', vista_admin, name = 'vista_admin'),
    path('', include('appPrincipal.urls')),
    path('rotiseria/', rotiseria, name = 'rotiseria'),
    path('abarrotes/', abarrotes, name = 'abarrotes'),
    path('productos/', productos, name = 'productos'),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_productos, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('carniceria/', carniceria, name = 'carniceria'),
    path('resumen_compra/', resumen_compra, name = 'resumen_compra'),
    path('confirmacion/', confirmacion, name = 'confirmacion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
