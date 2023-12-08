from django import forms
from appPrincipal.models import Clientes

class FormRegistro(forms.Form):
    rut = forms.CharField(max_length=10)
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField()
    fono = forms.CharField(max_length=10, required=False) 
    contraseña = forms.CharField(widget=forms.PasswordInput())
    validar_contraseña = forms.CharField(widget=forms.PasswordInput())

    rut.widget.attrs['class'] = 'form-control'
    nombre.widget.attrs['class'] = 'form-control'
    apellido.widget.attrs['class'] = 'form-control'
    fono.widget.attrs['class'] = 'form-control'
    email.widget.attrs['class'] = 'form-control'
    contraseña.widget.attrs['class'] = 'form-control'
    validar_contraseña.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        validar_contraseña = cleaned_data.get('validar_contraseña')

        if contraseña != validar_contraseña:
            self.add_error('contraseña', 'Las contraseñas no coinciden')
            self.add_error('validar_contraseña', 'Las contraseñas no coinciden')

class LoginForm(forms.Form):
    rut = forms.CharField(max_length = 10)
    contraseña = forms.CharField(widget = forms.PasswordInput())

    rut.widget.attrs['class'] = 'form-control'
    contraseña.widget.attrs['class'] = 'form-control'