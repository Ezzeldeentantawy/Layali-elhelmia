from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Layali_elhelmia.admin import admin_site
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path("admin/", admin_site.urls),
    path('', include('Layali_elhelmia.urls', namespace='Layali_elhelmia')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)