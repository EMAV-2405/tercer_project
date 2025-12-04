from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
import random

# Formularios
from .forms import (
    CustomLoginForm, CustomRegisterForm,
    obtener_form_por_categoria
)

# Modelos
from .models import (
    SUV, Deportivo, PickUp, Ford100Anios,
    CarritoItem, MetodoPago
)


# ================================
#   FUNCIONES DE NAVEGACIÓN
# ================================
def inicio(request):
    return render(request, 'inicio.html')


def catalogo(request, categoria):
    items = []
    titulo = ""
    template = 'catalogo.html'

    if categoria == 'suv':
        items = SUV.objects.all()
        titulo = "Nuestras SUVs"

    elif categoria == 'deportivo':
        items = Deportivo.objects.all()
        titulo = "Autos Deportivos"

    elif categoria == 'pickup':
        items = PickUp.objects.all()
        titulo = "Pick Ups Ford"

    elif categoria == '100anios':
        items = Ford100Anios.objects.all()
        template = '100anios.html'
        titulo = "Edición 100 Años Ford México"

    else:
        return redirect('inicio')

    return render(request, template, {
        'items': items,
        'titulo': titulo,
        'categoria': categoria
    })


# ================================
#      AUTENTICACIÓN
# ================================
def registro_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomRegisterForm()

    return render(request, 'auth.html', {
        'form': form,
        'tipo': 'Registro'
    })


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomLoginForm()

    return render(request, 'auth.html', {
        'form': form,
        'tipo': 'Iniciar Sesión'
    })


def logout_view(request):
    logout(request)
    return redirect('inicio')


# ================================
#       PERFIL DE USUARIO
# ================================
@login_required
def perfil_usuario(request):
    historial = MetodoPago.objects.filter(usuario=request.user).order_by('-fecha')

    tarjetas = historial.filter(tipo_pago='tarjeta').values('referencia').distinct()

    return render(request, 'perfil.html', {
        'historial': historial,
        'tarjetas': tarjetas
    })


# ================================
#     CARRITO Y PAGOS
# ================================
@login_required
def agregar_carrito(request, categoria, id_prod):
    modelos = {
        'suv': SUV,
        'deportivo': Deportivo,
        'pickup': PickUp,
        '100anios': Ford100Anios
    }

    model = modelos.get(categoria)
    if not model:
        return redirect('inicio')

    producto = get_object_or_404(model, id=id_prod)

    # Restricción especial
    if categoria == '100anios':
        if CarritoItem.objects.filter(usuario=request.user, tipo='100anios').exists():
            return render(request, 'error.html', {
                'mensaje': 'Solo puedes comprar 1 unidad de la Edición 100 Años.'
            })

    nombre = getattr(producto, 'nombre', "Edición 100 Años")

    CarritoItem.objects.create(
        usuario=request.user,
        nombre_producto=nombre,
        precio=producto.precio,
        tipo=categoria,
        producto_id=producto.id
    )

    # NUEVO: botón "Comprar Ahora"
    accion = request.GET.get('accion', 'agregar')

    if accion == 'comprar':
        return redirect('ver_carrito')

    return redirect('catalogo', categoria=categoria)


@login_required
def ver_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.precio for item in items)

    return render(request, 'carrito.html', {
        'items': items,
        'total': total
    })


@login_required
def eliminar_item(request, id_item):
    item = get_object_or_404(CarritoItem, id=id_item, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')


@login_required
def procesar_compra(request):
    if request.method == 'POST':
        items = CarritoItem.objects.filter(usuario=request.user)

        if not items:
            return redirect('catalogo', categoria='suv')

        total = sum(item.precio for item in items)
        tipo_pago = request.POST.get('metodo_pago')
        referencia_pago = request.POST.get('referencia_tarjeta', 'Pago en Efectivo')

        # Crear registro de pago
        pago = MetodoPago.objects.create(
            usuario=request.user,
            tipo_pago=tipo_pago,
            monto=total,
            referencia=referencia_pago
        )

        # Crear ticket antes de borrar carrito
        ticket_ctx = {
            'usuario': request.user,
            'fecha': timezone.now(),
            'folio': f"F-{random.randint(10000, 99999)}-{pago.id}",
            'items': list(items),
            'total': total,
            'metodo': tipo_pago,
            'referencia': referencia_pago
        }

        # Vaciar carrito
        items.delete()

        return render(request, 'ticket.html', ticket_ctx)

    return redirect('ver_carrito')


# ================================
#         CRUD GENERAL
# ================================
def obtener_modelo(categoria):
    modelos = {
        'suv': SUV,
        'deportivo': Deportivo,
        'pickup': PickUp,
        '100anios': Ford100Anios,
        'clientes': User,
        'pagos': MetodoPago
    }
    return modelos.get(categoria)


@staff_member_required(login_url='login')
def panel_gestion(request):
    return render(request, 'gestion/panel.html')


@staff_member_required(login_url='login')
def gestion_listar(request, categoria):
    modelo = obtener_modelo(categoria)
    if not modelo:
        return redirect('panel_gestion')

    items = modelo.objects.all()
    return render(request, 'gestion/listar.html', {
        'items': items,
        'categoria': categoria
    })


@staff_member_required(login_url='login')
def gestion_crear(request, categoria):
    FormClass = obtener_form_por_categoria(categoria)
    if not FormClass:
        return redirect('panel_gestion')

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_listar', categoria=categoria)
    else:
        form = FormClass()

    return render(request, 'gestion/formulario.html', {
        'form': form,
        'categoria': categoria,
        'accion': 'Crear'
    })


@staff_member_required(login_url='login')
def gestion_editar(request, categoria, id_obj):
    modelo = obtener_modelo(categoria)
    if not modelo:
        return redirect('panel_gestion')

    obj = get_object_or_404(modelo, id=id_obj)
    FormClass = obtener_form_por_categoria(categoria)

    if request.method == 'POST':
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion_listar', categoria=categoria)
    else:
        form = FormClass(instance=obj)

    return render(request, 'gestion/formulario.html', {
        'form': form,
        'categoria': categoria,
        'accion': 'Editar'
    })


@staff_member_required(login_url='login')
def gestion_eliminar(request, categoria, id_obj):
    modelo = obtener_modelo(categoria)
    if not modelo:
        return redirect('panel_gestion')

    obj = get_object_or_404(modelo, id=id_obj)
    obj.delete()

    return redirect('gestion_listar', categoria=categoria)
