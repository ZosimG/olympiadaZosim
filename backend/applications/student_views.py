import os.path
from django.shortcuts import get_object_or_404
from .models import Student, Application
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from applications.serializer_factory import get_student_serializer
from common.serializers import StudentSerializer
from common.base_view import BaseViewSet

class OneStudentViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        student = get_object_or_404(Student, pk=id)
        ser = StudentSerializer(student)
        return Response(ser.data)
    

class StudentViewSet(BaseViewSet, ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = get_student_serializer()
    def get(self, request):
        return super().list(request)
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = StudentSerializer(data=request.data)
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
        

class StudentFromOlympViewList(BaseViewSet, ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = get_student_serializer()#StudentSerializer

    def list(self, request, *args, **kwargs):
        # self.queryset = self.queryset.filter(olymp_id = kwargs.get('olymp_id', 1))
        # olymp = Olympiada.objects.filter(pk=kwargs.get('olymp_id', 1))
        students = Student.objects.filter(id__in=Application.objects.filter(olymp__id=kwargs.get('olymp_id', 1)).values_list("student__id", flat=True)).distinct()
        ser = get_student_serializer()#StudentSerializer(students, many=True)
        output = ser.data
        return Response(output)
    
        