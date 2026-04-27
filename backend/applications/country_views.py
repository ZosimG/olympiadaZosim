import os.path
from django.shortcuts import get_object_or_404
from .models import Country
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from applications.serializers import CountrySerializer

class OneCountryViewSet(APIView):
    def get(self, request, id, format=None):
        country = get_object_or_404(Country, pk=id)
        ser = CountrySerializer(country)
        output = ser.data
        return Response(output)

    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        if request.method == 'DELETE':
            country = get_object_or_404(Country, pk=id)
            try:
                output["country"] = country.id
                country.delete()
                output["message"] = 'Успешно!'
            except:
                del output["olympiada"]
                output["valid"] = False
                output["message"] = 'Ошибка!'
            return Response(output)

    def put(self, request, id, format=None):
        output = {"valid": False}
        country = get_object_or_404(Country, pk=id)
        ser = CountrySerializer(country, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = CountrySerializer(data=request.data)
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
