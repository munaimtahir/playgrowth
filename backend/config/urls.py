from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({'status': 'ok', 'service': 'playgrowth-copilot'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
    path('api/v1/', include('growth.urls')),
]
