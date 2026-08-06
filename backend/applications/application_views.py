import os.path
from django.shortcuts import get_object_or_404
from applications.models import Application
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from applications.parse_applications import ApplicationParser
from common.serializers import ApplicationSerializer
from applications.serializers import ApplicationStatusSerializer, AppplicationsStatusSertializerMultiple
from common.base_view import BaseViewSet

class OneApplicationViewSet(BaseViewSet):
    def get(self, request, id, format=None):
        application = get_object_or_404(Application, pk=id)
        ser = ApplicationSerializer(application)
        output = ser.data
        output["olymp_name"] = application.olymp.olymp_name
        return Response(output)
    
    def delete(self, request, id, format=None):
        output = {"valid": True, "message": ''}
        application = get_object_or_404(Application, pk=id)
        try:
            output["application"] = application.id
            application.delete()
            output["message"] = 'Заявка успешно удалена'
        except Exception:
            del output["application"]
            output["valid"] = False
            output["message"] = 'Ошибка при удалении'
        return Response(output)

    def put(self, request, id, format=None):
        application = get_object_or_404(Application, pk=id)
        ser = ApplicationSerializer(application, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(BaseViewSet, ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer   
    
    def get(self, request):
        return super().list(request) 
    
    def post(self, request):
        output = {"valid": False, "message": ""}
        ser = ApplicationSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            output["valid"] = True
            output["message"] = "Заявка успешно создана"
            output["data"] = ser.data
            return Response(output, status=status.HTTP_201_CREATED)
        output["message"] = 'Проверьте правильность заполнения формы'
        output["errors"] = ser.errors
        return Response(output, status=status.HTTP_400_BAD_REQUEST)


class ChangeApplicationStatus(BaseViewSet):
    def put(self, request, id, format=None):
        application = get_object_or_404(Application, pk=id)
        ser = ApplicationStatusSerializer(application, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeApplicationStatusMultiple(BaseViewSet):
    def put(self, request, format=None):
        ser = ApplicationsStatusSerializerMultiple(data=request.data)
        if ser.is_valid():
            status_dict = ser.validated_data['status_dict']
            for app_id, new_status in status_dict.items():
                application = get_object_or_404(Application, pk=app_id)
                application.status = new_status
                application.save()
            return Response({"message": "Статусы успешно обновлены", "updated": len(status_dict)})
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationUploadView(BaseViewSet):
    parser_classes = [FileUploadParser]
    
    def put(self, request, olymp_id, filename, format=None):
        folder = 'folder'
        result = {"error": "", "success": ""}
        file_obj = request.data['file']
        full_path = os.path.join(folder, filename)
        with open(full_path, 'wb') as f:
            f.write(file_obj.read())
        olympiada = get_object_or_404(Olympiada, pk=olymp_id)
        employee = get_object_or_404(Employee, user=request.user)
        result["error"] = ApplicationParser.parse_excel(full_path, olympiada, employee)
        if not result["error"]:
            result["success"] = "Файл успешно обработан"
        return Response(result)
