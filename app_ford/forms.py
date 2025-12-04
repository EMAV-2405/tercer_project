from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Modelos (todos en un solo lugar)
from .models import SUV, Deportivo, PickUp, Ford100Anios, MetodoPago

# --- Formulario de Login Estilizado ---
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-style',
        'placeholder': 'Nombre de usuario'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-style',
        'placeholder': 'Contraseña'
    }))


# --- Formulario de Registro Estilizado ---
class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)

        # Aplicar estilos a cada campo
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'input-style',
                'placeholder': self.fields[field].label
            })


# --- Formularios del CRUD para vehículos ---
class SUVForm(forms.ModelForm):
    class Meta:
        model = SUV
        fields = '__all__'


class DeportivoForm(forms.ModelForm):
    class Meta:
        model = Deportivo
        fields = '__all__'


class PickUpForm(forms.ModelForm):
    class Meta:
        model = PickUp
        fields = '__all__'


class Ford100AniosForm(forms.ModelForm):
    class Meta:
        model = Ford100Anios
        fields = '__all__'


# --- Formularios adicionales ---
# Formulario para Clientes (editar usuarios desde el panel de gestión)
class ClienteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        labels = {
            'is_staff': '¿Es Administrador?',
            'is_active': '¿Cuenta Activa?'
        }

# Formulario para Historial de Pagos
class PagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = '__all__'


# --- Diccionario / Selector único de formulario por categoría ---
def obtener_form_por_categoria(categoria):
    """
    Devuelve la clase Form correspondiente a la 'categoria' recibida.
    Categorias válidas: 'suv', 'deportivo', 'pickup', '100anios', 'clientes', 'pagos'
    """
    mapping = {
        'suv': SUVForm,
        'deportivo': DeportivoForm,
        'pickup': PickUpForm,
        '100anios': Ford100AniosForm,
        'clientes': ClienteForm,
        'pagos': PagoForm,
    }
    return mapping.get(categoria)
