import os.path
from django.shortcuts import get_object_or_404
from applications.models import Application
from users.models import Employee
from applications.models import Team
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from applications.parse_applications import ApplicationParser
from common.serializers import ApplicationSerializer
from common.serializers import TeamSerializer
from common.base_view import BaseViewSet



class TeamViewSet(BaseViewSet, ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        ser = TeamSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class OneTeamViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        team = get_object_or_404(Team, pk=id)
        ser = TeamSerializer(team)
        return Response(ser.data)
    
    def delete(self, request, id, format=None):
        team = get_object_or_404(Team, pk=id)
        team.delete()
        return Response({"message": "Команда удалена"}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id, format=None):
        team = get_object_or_404(Team, pk=id)
        ser = TeamSerializer(team, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)