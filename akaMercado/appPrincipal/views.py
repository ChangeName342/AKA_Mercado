from django.shortcuts import render, redirect, HttpResponse
from appPrincipal.forms import FormRegistro
from appPrincipal.models import Clientes, Productos, Administradores, Clientes, Pedidos, Productos_has_Pedidos
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from appPrincipal.Carrito import Carrito
from datetime import datetime
from django.contrib.auth.models import User 

# Create your views here.
def index(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            fono = form.cleaned_data.get('fono', None)
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']

            cliente = Clientes(rut=rut, nombre=nombre, apellido=apellido, fono=fono, email=email, contraseña=contraseña)
            cliente.save()

            return redirect('home') 

    else:
        form = forms.FormRegistro()

    return render(request, 'registro.html', {'form':form})

def login_admin(request):
    if request.method == 'POST':
        try:
            detalleAdmin = Administradores.objects.get(email=request.POST['email'], contraseña=request.POST['contraseña'])
            if detalleAdmin.rol == "Administrador":
                print("Administrador=", detalleAdmin)
                request.session['email'] = detalleAdmin.email
                return redirect('vista_admin')
            else:
                messages.error(request, 'No tienes permiso para acceder a esta página')
        except ObjectDoesNotExist:
            messages.success(request, 'Nombre de usuario o password no es correcto...!')
    return render(request, 'login_admin.html')

def login_cliente(request):
    if request.method == 'POST':
        try:
            detalleUsuario = Clientes.objects.get(email = request.POST['email'], contraseña = request.POST['contraseña'])
            if detalleUsuario.rol == "Cliente":
                print("Usuario=", detalleUsuario)
                request.session['email'] = detalleUsuario.email
                return redirect('vista_cliente')
            else:
                messages.error(request, 'No tienes permiso para acceder a esta página')
        except ObjectDoesNotExist:
            messages.success(request, 'Nombre de usuario o password no es correcto...!')
    return render(request,'login_cliente.html')

def cerrar_sesion(request):
    try:
        del request.session['email']
    except:
        return render(request, 'home.html')
    return render(request, 'home.html')

def vista_cliente(request):
    return render(request, 'home_cliente.html')

def vista_admin(request):
    productos = Productos.objects.all()
    messages.success(request, 'Productos listados!')
    return render(request, 'gestion_productos.html', {'productos': productos})

def registrar_producto(request):
    if request.method == 'POST':
        idProd = int(request.POST['idProd'])
        if idProd < 0:
            messages.error(request, 'El ID del producto no puede ser negativo.')
            return redirect('vista_admin') 
        nombre = request.POST['nombre']
        precio = float(request.POST['precio'])
        if precio < 0:
            messages.error(request, 'El precio del producto no puede ser negativo.')
            return redirect('vista_admin')  
        imagen = request.FILES.get('imagen')
        cantidad = int(request.POST['cantidad'])
        if cantidad < 0:
            messages.error(request, 'La cantidad del producto no puede ser negativa.')
            return redirect('vista_admin') 
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']
        categorias_permitidas = ['Rotisería', 'Abarrotes', 'Carnicería']
        if categoria not in categorias_permitidas:
            messages.error(request, 'La categoría ingresada no es válida. Debe ser Rotisería, Abarrotes o Carnicería')
            return redirect('vista_admin')  
        producto = Productos.objects.create(
            idProd=idProd, nombre=nombre, precio=precio, imagen=imagen, cantidad=cantidad, descripcion=descripcion, categoria=categoria)
        messages.success(request, 'Producto registrado!')
        return redirect('vista_admin')
    
def edicion_producto(request, idProd):
    producto = Productos.objects.get(idProd = idProd)
    return render(request, "edicion_producto.html", {"producto": producto})


def editar_producto(request):
    if request.method == 'POST':
        idProd = int(request.POST['idProd'])
        if idProd < 0:
           
            messages.error(request, 'El ID del producto no puede ser negativo.')
            return redirect('vista_admin') 

        nombre = request.POST['nombre']
        precio = float(request.POST['precio'])
        if precio < 0:
          
            messages.error(request, 'El precio del producto no puede ser negativo.')
            return redirect('vista_admin') 

        imagen = request.FILES.get('imagen')
        cantidad = int(request.POST['cantidad'])
        if cantidad < 0:
            
            messages.error(request, 'La cantidad del producto no puede ser negativa.')
            return redirect('vista_admin') 

        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']

        
        categorias_permitidas = ['Rotisería', 'Abarrotes', 'Carnicería']
        if categoria not in categorias_permitidas:
            
            messages.error(request, 'La categoría ingresada no es válida. Debe ser Rotisería, Abarrotes o Carnicería')
            return redirect('vista_admin')  

        producto = Productos.objects.get(idProd=idProd)
        producto.nombre = nombre
        producto.precio = precio
        producto.imagen = imagen
        producto.cantidad = cantidad
        producto.descripcion = descripcion
        producto.categoria = categoria

        producto.save()

        messages.success(request, 'Producto actualizado!')
        return redirect('vista_admin')
    
def eliminar_producto(request, idProd):
    producto = Productos.objects.get(idProd = idProd)
    producto.delete()

    messages.success(request, 'Producto eliminado!')

    return redirect('vista_admin')

def rotiseria(request):
    productos_rotiseria = Productos.objects.filter(categoria='Rotisería')
    return render(request, 'rotiseria.html', {'productos_rotiseria': productos_rotiseria})

def abarrotes(request):
    productos_abarrotes = Productos.objects.filter(categoria='Abarrotes')
    return render(request, 'abarrotes.html', {'productos_abarrotes': productos_abarrotes})

def carniceria(request):
    productos_carniceria = Productos.objects.filter(categoria='Carnicería')
    return render(request, 'carniceria.html', {'productos_carniceria': productos_carniceria})

def productos(request):
    productos = Productos.objects.all()
    return render(request, 'productos.html', {'productos' : productos})

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(idProd=producto_id)
    carrito.agregar(producto)
    return redirect("productos")

def eliminar_productos(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(idProd=producto_id)
    carrito.eliminar(producto)
    return redirect("productos")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Productos.objects.get(idProd = producto_id)
    carrito.restar(producto)
    return redirect("productos")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("productos")

def gestion_clientes(request):
    clientes = Clientes.objects.all()
    messages.success(request, 'Clientes listados!')
    return render(request, 'gestion_clientes.html', {'clientes': clientes})

def registrar_cliente(request):
    rut = request.POST['rut']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    fono = request.POST['fono']
    email = request.POST['email']
    contraseña = request.POST['contraseña']

    cliente = Clientes.objects.create(rut = rut, nombre = nombre, apellido = apellido, fono = fono, email = email, contraseña = contraseña)
    messages.success(request, 'Cliente registrado!')
    return redirect('vista_admin')

def edicion_cliente(request, rut):
    cliente = Clientes.objects.get(rut = rut)
    return render(request, "edicion_cliente.html", {"cliente": cliente})

def editar_cliente(request):
    rut = request.POST['rut']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    fono = request.POST['fono']
    email = request.POST['email']
    contraseña = request.POST['contraseña']

    cliente = Clientes.objects.get(rut = rut)
    cliente.nombre = nombre
    cliente.apellido = apellido
    cliente.fono = fono
    cliente.email = email
    cliente.contraseña = contraseña

    cliente.save()

    messages.success(request, 'Datos del cliente actualizados!')
    return redirect('vista_admin')

def eliminar_cliente(request, rut):
    cliente = Clientes.objects.get(rut = rut)
    cliente.delete()

    messages.success(request, 'Cliente eliminado!')

    return redirect('vista_admin')

def resumen_compra(request):
    carrito = request.session.get('carrito', {})
    productos_pedido = []

    for producto_id, item in carrito.items():
        producto = Productos.objects.get(idProd=producto_id)
        precio_unitario = item['acumulado'] / item['cantidad']
        detalle_producto = {
            'nombre': producto.nombre,
            'cantidad': item['cantidad'],
            'precio_unitario': precio_unitario,
            'precio_total': item['acumulado']
        }
        productos_pedido.append(detalle_producto)

    return render(request, 'resumen.html', {'productos_pedido': productos_pedido})

def confirmacion(request):
    return render(request, 'confirmacion.html')