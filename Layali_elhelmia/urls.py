from django.contrib import admin
from django.urls import path, include
from .admin import admin_site
from django.conf.urls.static import static
from django.conf import settings
from . import views



app_name = 'Layali_elhelmia'

urlpatterns = [
    path("Layali-elhelmia_admin/", admin_site.urls),
    path('', views.homepage, name='home'),
    path('menu/', views.menu, name='menu'),
    path('menu/cart/', views.cart, name='cart'),
    path('menu_en/cart_en/', views.cart, name='cart_en'),
    path('menu_en/', views.menu, name='menu_en'),
    path('reset_meals_sales' , views.reset_meals_sales, name='reset_meals_sales'),
    # Other URL patterns...
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)