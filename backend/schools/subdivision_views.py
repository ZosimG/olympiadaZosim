import os.path
from django.shortcuts import get_object_or_404
from .models import Subdivision
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from schools.serializers import SubdivisionSerializer
from .parse_subdivisions import SubdivisionParser
from common.base_view import BaseViewSet


class OneSubdivisionViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        #id = request.GET['id']
        subdivision = get_object_or_404(Subdivision, pk=id)
        ser = SubdivisionSerializer(subdivision)
        return Response(ser.data)
    
    def put(self, request, id, format=None):
        output = {"valid": False}
        subdivision = get_object_or_404(Subdivision, pk=id)
        ser = SubdivisionSerializer(subdivision, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)

class SubdivisionViewSet(BaseViewSet, ModelViewSet):
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializer
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = SubdivisionSerializer(data=request.data, many=True)
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

class SubdivisionFileUploadView(BaseViewSet):
    parser_classes = [FileUploadParser]
    def put(self, request, filename, format=None):
        folder='folder'
        result = {"error": ""}
        file_obj = request.data['file']
        full_path = os.path.join(folder, filename)
        with open(full_path, 'wb') as f:
            f.write(file_obj.read())
        result["error"] += SubdivisionParser.parse_excel(full_path)
        return Response(result)