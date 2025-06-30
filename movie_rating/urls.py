from django.contrib import admin
from django.urls import include, path
from peliculas.views import import_peliculas 
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')), # Users app urls
    
    path('api/auth/', include('users.urls')),  
    path('api/', include('peliculas.urls')),
    path('api/peliculas/import/', import_peliculas, name='import_peliculas'),
]
