from rest_framework import serializers
from schools.serializers import SchoolSerializer, SubdivisionSerializer 
from applications.models import Student
from olymp.models import Olympiada
from schools.models import Subdivision, School
from applications.models import Application


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Student
        fields = ['id', 'name', 'birthday', 'course_study', 'special_needs', 'contact_phone', 'country', 'sex']


class OlympSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Olympiada
        fields = ['id', 'olymp_name', 'olymp_date_start', 'olymp_time']   #No creators yet!


class ApplicationSerializer(serializers.ModelSerializer):
    
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source="student", write_only=True)
    olymp = OlympSerializer(read_only=True)
    olymp_id = serializers.PrimaryKeyRelatedField(queryset=Olympiada.objects.all(), source="olymp", write_only=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), source="school", write_only=True)
    subdivision = SubdivisionSerializer(read_only=True)
    subdivision_id = serializers.PrimaryKeyRelatedField(queryset=Subdivision.objects.all(), source="subdivision", write_only=True)

    class Meta:
        model = Application
        fields = ['id', 'student', 'student_id', 'olymp', 'olymp_id', 'date', 'employee', 'status', 'participate', 'school', 'school_id', 'teacher', 'subdivision', 'subdivision_id']
