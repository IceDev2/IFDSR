from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('', include('core.urls')),
    re_path(r"^.*$", landing),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def landing(_):
    return HttpResponse("ok")  # tidak pakai template biar gak drama

