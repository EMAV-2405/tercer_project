from django.db import models
from django.contrib.auth.models import User

# --- 1. Tablas de Vehículos ---
class SUV(models.Model):
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField()
    color = models.CharField(max_length=50)
    motor = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    imagen_url = models.URLField(max_length=500)

    def __str__(self): return self.nombre

class Deportivo(models.Model):
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField()
    color = models.CharField(max_length=50)
    motor = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    imagen_url = models.URLField(max_length=500)

    def __str__(self): return self.nombre

class PickUp(models.Model):
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField()
    color = models.CharField(max_length=50)
    motor = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    imagen_url = models.URLField(max_length=500)

    def __str__(self): return self.nombre

class Ford100Anios(models.Model):
    # Edición especial: Campos específicos
    motor = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default="Azul Centenario")
    rines = models.CharField(max_length=100)
    emblemas = models.CharField(max_length=200)
    interior = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen_url = models.URLField(max_length=500)

    def __str__(self): return "Edición 100 Años Ford"

# --- 2. Carrito y Ventas ---
class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=50) # 'suv', 'deportivo', 'pickup', 'aniversario'
    producto_id = models.IntegerField()
    
    def __str__(self): return f"{self.nombre_producto} - {self.usuario.username}"

class MetodoPago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50, choices=[('tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')])
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    estado_pago = models.CharField(max_length=50, default="Exitoso")

    def __str__(self): return f"Pago {self.id} - {self.usuario}"