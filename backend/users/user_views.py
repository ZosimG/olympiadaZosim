import os.path
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.expressions import result
from django.shortcuts import get_object_or_404
from users.models import ROLES
from applications.models import sex
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserSerializer_confident
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from common.base_view import BaseViewSet


class OneUserViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        permission_classes = [AllowAny]
        #id = request.GET['id']
        user = get_object_or_404(User, pk=id)
        ser = UserSerializer(user)
        return Response(ser.data)

class UserViewSet(BaseViewSet, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer_confident
    def get(self, request):
        #permission_classes = [permissions.IsAuthenticated]
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = UserSerializer(data=request.data)
                if ser.is_valid():
                    user = User.objects.create_user(
                        ser.initial_data['username'],
                        ser.initial_data['email'],
                        ser.initial_data['password']
                    )
                    output["valid"] = True
                    output["user_id"] = user.id
                else:
                    output["valid"] = False
                    output['msg'] = 'Проверьте правильность заполнения формы'
            except Exception as e:
                output['valid'] = False
                output['msg'] = 'Ошибка при сохранении'
        return Response(output)


class GenderViewList(BaseViewSet):
    def get(self, request):
        sex_dict = dict(sex)
        return Response(sex_dict)

class RoleViewList(BaseViewSet):
    def get(self, request):
        role_dict = dict(ROLES)
        return Response(role_dict)
