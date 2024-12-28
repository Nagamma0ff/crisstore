from django.urls import path
from tienda import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('resumen-pedido/', views.resumen_pedido, name='resumen_pedido'),
    path('confirmacion-pedido/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('contacto/', views.contacto, name='contacto'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('admin/', admin.site.urls),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)