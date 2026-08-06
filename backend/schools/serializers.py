from rest_framework import serializers
from schools.models import School
from schools.models import Subdivision

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

    
class SubdivisionSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Subdivision
        fields = ['id', 'subdivision_name']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = School
        fields = ['id', 'school_name', 'school_subdivision']

