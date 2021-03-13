from django.contrib import admin
from django.urls import path, include

from APPS.RBAC import urls as rbac

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO DEMO ↓
    path('v1/RBAC/', include(rbac))
]
