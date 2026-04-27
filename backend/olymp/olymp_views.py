import os.path
from django.shortcuts import get_object_or_404
from .models import Olympiada
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from common.serializers import OlympSerializer

class OneOlympViewSet(APIView):
    def get(self, request, id, format=None):
        #id = request.GET['id']
        olympiada = get_object_or_404(Olympiada, pk=id)
        ser = OlympSerializer(olympiada)
        return Response(ser.data)

    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        if request.method == 'DELETE':
            olympiada = get_object_or_404(Olympiada, pk=id)
            try:
                output["olympiada"] = olympiada.id
                olympiada.delete()
                output["message"] = 'Успешно!'
            except:
                del output["olympiada"]
                output["valid"] = False
                output["message"] = 'Ошибка!'
            return Response(output)

    def put(self, request, id, format=None):
        output = {"valid": False}
        olympiada = get_object_or_404(Olympiada, pk=id)
        ser = OlympSerializer(olympiada, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)

class OlympViewSet(ModelViewSet):
    queryset = Olympiada.objects.all()
    serializer_class = OlympSerializer
    
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        # ser = OlympSerializer(olympiada, request.data)
        if request.method == "POST":
            try:
                ser = OlympSerializer(data=request.data)
                if ser.is_valid():
                    ser.save()
                    output["valid"] = True
                else:
                    output["valid"] = False
                    output['msg'] = 'Проверьте правильность заполнения формы'
            except Exception as e:
                output['valid'] = False
                output['msg'] = 'Ошибка при сохранении'
        return Response(output)

