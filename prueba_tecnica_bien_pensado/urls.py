"""
URL configuration for prueba_tecnica_bien_pensado project.

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
from django.urls import path
from bodegas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('listar_bodegas/', views.listar_bodegas_ordenadas, name='listar_bodegas'),
    path('crear_bodega/', views.crear_bodega, name='crear_bodega'),
    path('listar_productos_total_descendente/', views.listar_productos_total_descendente,
         name='listar_productos_total_descendente'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('insertar_actualizar_inventario/', views.insertar_actualizar_inventario,
         name='insertar_actualizar_inventario'),
    path('trasladar_producto/', views.trasladar_producto,
         name='trasladar_producto'),
]
