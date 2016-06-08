from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from .permissions import IsAdminOrOwner
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    # noinspection PyRedundantParentheses
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAdminOrOwner())
