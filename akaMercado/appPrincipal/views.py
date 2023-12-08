from django.shortcuts import render, redirect
from appPrincipal.forms import FormRegistro
from appPrincipal.models import Clientes, Productos, Administradores
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


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
    return render(request, 'vista_cliente.html')

def vista_admin(request):
    productos = Productos.objects.all()
    messages.success(request, 'Productos listados!')
    return render(request, 'gestion_productos.html', {'productos': productos})

def registrar_producto(request):
    idProd = request.POST['idProd']
    nombre = request.POST['nombre']
    precio = request.POST['precio']
    imagen = request.FILES.get('imagen')
    cantidad = request.POST['cantidad']
    descripcion = request.POST['descripcion']
    categoria = request.POST['categoria']

    producto = Productos.objects.create(
        idProd = idProd, nombre = nombre,precio = precio, imagen = imagen, cantidad = cantidad, descripcion = descripcion, categoria = categoria)
    messages.success(request, 'Producto registrado!')
    return redirect('vista_admin')

def edicion_producto(request, idProd):
    producto = Productos.objects.get(idProd = idProd)
    return render(request, "edicion_producto.html", {"producto": producto})


def editar_producto(request):
    idProd = request.POST['idProd']
    nombre = request.POST['nombre']
    precio = request.POST['precio']
    imagen = request.FILES.get('imagen')
    cantidad = request.POST['cantidad']
    descripcion = request.POST['descripcion']
    categoria = request.POST['categoria']

    producto = Productos.objects.get(idProd = idProd)
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