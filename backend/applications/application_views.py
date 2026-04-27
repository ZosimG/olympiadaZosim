import os.path
from django.shortcuts import get_object_or_404
from applications.models import Application
from users.models import Employee
from applications.models import Olympiada
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from applications.parse_applications import ApplicationParser
from common.serializers import ApplicationSerializer
from applications.serializers import ApplicationStatusSerializer, AppplicationsStatusSertializerMultiple

class OneApplicationViewSet(APIView):
    def get(self, request, id, format=None):
        application = get_object_or_404(Application, pk=id)
        ser = ApplicationSerializer(application)
        output = ser.data
        output["Название"] = application.olymp.olymp_name
        return Response(output)
    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        if request.method == "DELETE":
            application = get_object_or_404(Application, pk=id)
            try:
                output["application"] = application.id
                application.delete()
                output["message"] = 'Успешно!'
            except:
                del output["application"]
                output["valid"] = False
                output["message"] = 'Ошибка!'
            return Response(output)

    def put(self, request, id, format=None):
        application = get_object_or_404(Application, pk=id)
        ser = ApplicationSerializer(application, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer   
    def get(self, request):
        return super().list(request) 
    
    def post(self, request):
        output = {"valid": False}
        if request.method == "POST":
            try:
                ser = ApplicationSerializer(data=request.data)
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

class ChangeApplicationStatus(APIView):
    def put(self, request, id, format=None):
        if request.method == "PUT":
            application = get_object_or_404(Application, pk=id)
            ser = ApplicationStatusSerializer(application, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Error")

class ChangeApplicationStatusMultiple(APIView):
    def put(self, request, format=None):
        if request.method == "PUT":
            ser = AppplicationsStatusSertializerMultiple(data=request.data)
            if ser.is_valid():
                for key in ser["status_dict"].value:
                    # print(key, ser["status_dict"].value[key])
                    application = get_object_or_404(Application, pk=key)
                    application.application_status = ser["status_dict"].value[key]
                    application.save()
                # print(ser["status_dict"].value)
                return Response(ser.data)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Error")

class ApplicationUploadView(APIView):
    parser_classes = [FileUploadParser]
    def put(self, request, olymp_id, filename, format=None):
        folder='folder'
        result = {"error": ""}

        file_obj = request.data['file']
        full_path = os.path.join(folder, filename)
        with open(full_path, 'wb') as f:
            f.write(file_obj.read())
        olympiada = get_object_or_404(Olympiada, pk=olymp_id)
        employee = get_object_or_404(Employee, user__id=request.user.id)
        result["error"] += ApplicationParser.parse_excel(full_path, olympiada, employee)
        return Response(result)