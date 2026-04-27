from rest_framework import serializers

from applications.models import Student
from applications.models import Application
from applications.models import Country
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


gender = serializers.SerializerMethodField('')

def getGender(self, obj):
    return obj.sex.username






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
