from django.contrib import admin
from .models import SUV, Deportivo, PickUp, Ford100Anios, MetodoPago

@admin.register(SUV)
class SUVAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'anio', 'color')

@admin.register(Deportivo)
class DeportivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'anio', 'color')

@admin.register(PickUp)
class PickUpAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'anio', 'color')

@admin.register(Ford100Anios)
class AniversarioAdmin(admin.ModelAdmin):
    list_display = ('motor', 'color', 'disponible', 'precio')

@admin.register(MetodoPago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_pago', 'monto', 'fecha')