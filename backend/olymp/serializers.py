from rest_framework import serializers
from applications.models import Student, Application
from olymp.models import Participant
from olymp.models import Olympiada
from olymp.models import Result
# from applications.serializers import ApplicationSerializer, StudentSerializer
from applications.serializer_factory import get_application_serializer, get_student_serializer
from common.serializers import ApplicationSerializer, StudentSerializer

# from django.contrib.auth.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ParticipantSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Participant
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'