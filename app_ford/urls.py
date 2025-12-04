from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Catálogo
    path('catalogo/<str:categoria>/', views.catalogo, name='catalogo'),
    
    # Auth
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Carrito
    path('agregar/<str:categoria>/<int:id_prod>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar/<int:id_item>/', views.eliminar_item, name='eliminar_item'),
    path('checkout/', views.procesar_compra, name='procesar_compra'),

# ... tus rutas anteriores ...

    # RUTAS DE GESTIÓN (ADMIN PERSONALIZADO)
    path('gestion/', views.panel_gestion, name='panel_gestion'),
    path('gestion/<str:categoria>/', views.gestion_listar, name='gestion_listar'),
    path('gestion/<str:categoria>/crear/', views.gestion_crear, name='gestion_crear'),
    path('gestion/<str:categoria>/editar/<int:id_obj>/', views.gestion_editar, name='gestion_editar'),
    path('gestion/<str:categoria>/eliminar/<int:id_obj>/', views.gestion_eliminar, name='gestion_eliminar'),

]