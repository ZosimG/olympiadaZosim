import os.path
from django.shortcuts import get_object_or_404
from .models import Result
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import ResultSerializer
from common.base_view import BaseViewSet

class OneResultViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        #id = request.GET['id']
        result = get_object_or_404(Result, pk=id)
        ser = ResultSerializer(result)
        return Response(ser.data)
    
    def put(self, request, id, format=None):
        output = {"valid": False}
        result = get_object_or_404(Result, pk=id)
        ser = ResultSerializer(result, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)

class ResultViewSet(BaseViewSet, ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = ResultSerializer(data=request.data, many=True)
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