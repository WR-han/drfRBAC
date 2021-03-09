from rest_framework import serializers

from APPS.RBAC.models import RBACUser


class RBACUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RBACUser
        fields = "__all__"
