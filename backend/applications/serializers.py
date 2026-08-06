from rest_framework import serializers
from applications.models import Student
from applications.models import Application
from applications.models import Country, Applicant
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

gender = serializers.SerializerMethodField('')

def getGender(self, obj):
    return obj.sex.username




class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['id', 'student', 'team']

    def validate(self, data):
        if not data.get('student') and not data.get('team'):
            raise serializers.ValidationError("Должен быть указан либо студент, либо команда")
        if data.get('student') and data.get('team'):
            raise serializers.ValidationError("Нельзя указать и студента, и команду одновременно")
        return data


class ApplicationStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Application
        fields = ['status']


class AppplicationsStatusSertializerMultiple(serializers.Serializer):
    status_dict = serializers.DictField(child=serializers.IntegerField())


class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['id', 'country_name']
