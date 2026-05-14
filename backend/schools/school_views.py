import os.path
from django.shortcuts import get_object_or_404
from .models import School
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from schools.serializers import SchoolSerializer
from .parse_schools import SchoolParser
from common.base_view import BaseViewSet


class OneSchoolViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        school = get_object_or_404(School, pk=id)
        ser = SchoolSerializer(school)
        return Response(ser.data)
    
    def put(self, request, id, format=None):
        output = {"valid": False}
        school = get_object_or_404(School, pk=id)
        ser = SchoolSerializer(school, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)
    
    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        if request.method == "DELETE":
            school = get_object_or_404(School, pk=id)
            apps = school.schools.all()
            try:
                if (len(apps) != 0):
                    raise Exception
                else:
                    output["school"] = school.id
                    school.delete()
                    output["message"] = 'Успешно!'
            except:
                del output["school"]
                output["valid"] = False
                output["message"] = 'Ошибка!'
            return Response(output)

class SchoolViewSet(BaseViewSet, ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
    def get(self, request):
        return super().list(request)
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = SchoolSerializer(data=request.data)
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

class FileUploadView(BaseViewSet):
    parser_classes = [FileUploadParser]
    def put(self, request, filename, format=None):
        folder='folder'
        result = {"error": ""}

        file_obj = request.data['file']
        full_path = os.path.join(folder, filename)
        with open(full_path, 'wb') as f:
            f.write(file_obj.read())
        result["error"] += SchoolParser.parse_excel(full_path)
        return Response(result)