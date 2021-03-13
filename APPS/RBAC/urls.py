from rest_framework import routers

from APPS.RBAC.views import Users

router = routers.SimpleRouter()
# TODO DEMO ↓
router.register('user', Users)

urlpatterns = []

urlpatterns += router.urls
