"""webservice_tienda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from .views import * 
import webservice_tienda.settings as settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tipo_producto', TipoProductoApi.as_view()),
    path('producto', ProductoApi.as_view()),
    path('tipo_usuario', TipoUsuarioApi.as_view()),
    path('usuario', UsuarioApi.as_view()),
    path('venta', VentaApi.as_view()),
    path('detalle_venta', ProductoVentaApi.as_view()),
    path('pais', PaisApi.as_view()),
    path('ciudad', CiudadApi.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
