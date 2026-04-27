import os.path
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view

from .models import Employee
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from users.serializers import EmployeeSerializer

class OneEmployeeViewSet(APIView):
    def get(self, request, id, format=None):
        employee = get_object_or_404(Employee, pk=id)
        ser = EmployeeSerializer(employee)
        return Response(ser.data)
    
    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        if request.method == 'DELETE':
            employee = get_object_or_404(Employee, pk=id)
            try:
                output["employee"] = employee.id
                employee.delete()
                output["message"] = 'Успешно!'
            except:
                del output["employee"]
                output["valid"] = False
                output["message"] = 'Ошибка!'
            return Response(output)
        
    def put(self, request, id, format=None):
        output = {"valid": False}
        employee = get_object_or_404(Employee, pk=id)
        ser = EmployeeSerializer(employee, data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
        return Response(output)

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get(self, request):
        #permission_classes = [permissions.IsAuthenticated]
        return super().list(request)
        
    # @extend_schema(
    #     request=EmployeeSerializer
    # )
    # @api_view(["POST"])
    
    def post(self, request):
        output = {"valid": False}
        # ser = EmployeeSerializer(olympiada, request.data)
        if request.method == "POST":
            try:
                ser = EmployeeSerializer(data=request.data)
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
