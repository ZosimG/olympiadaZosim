from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import AllowAny

class BaseViewSet(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [HasAPIKey()]
        return super().get_permissions()
