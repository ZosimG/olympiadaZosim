from rest_framework import serializers
from applications.models import Student, Application
from olymp.models import Participant
from olymp.models import Olympiada
from olymp.models import Result
# from applications.serializers import ApplicationSerializer, StudentSerializer
from applications.serializer_factory import get_application_serializer, get_student_serializer

# from django.contrib.auth.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)





class ParticipantSerializer(serializers.ModelSerializer):
    
    student = get_student_serializer()#StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source="student", write_only=True)
    application = get_application_serializer()#ApplicationSerializer(read_only=True)
    application_id = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all(), source="application", write_only=True)

    class Meta:
        
        model = Participant
        fields = ['id', 'student', 'student_id', 'application', 'application_id']

class ResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    participant_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source="student", write_only=True)

    class Meta:
        
        model = Result
        fields = ['id', 'participant', 'participant_id', 'task_number', 'result_value']
