from django.urls import path
from rest_framework import routers

from APPS.RBAC.views import Users, Login

router = routers.SimpleRouter()
# TODO DEMO ↓
router.register('user', Users)

urlpatterns = [
    # TODO LOGIN DEMO ↓
    path('Login/', Login.as_view()),
]

urlpatterns += router.urls
