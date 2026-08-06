from rest_framework import serializers
from schools.serializers import SchoolSerializer, SubdivisionSerializer 
from applications.models import Student
from olymp.models import Olympiada, Participant
from schools.models import Subdivision, School
from applications.models import Application, Team, Applicant
from applications.serializers import ApplicantSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Student
        fields = ['id', 'name', 'birthday', 'course_study', 'special_needs', 'contact_phone', 'country', 'sex']


class OlympSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Olympiada
        fields = ['id', 'olymp_name', 'olymp_date_start', 'olymp_time']   #No creators yet!


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(required=True)
    olymp_name = serializers.CharField(source='olymp.olymp_name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        applicant_data = validated_data.pop('applicant')
        application = Application.objects.create(**validated_data)
        
        # Создаём заявителя
        applicant = Applicant.objects.create(application=application, **applicant_data)
        
        # Создаём участников (Participant) через сигнал или вручную
        if applicant.student:
            Participant.objects.get_or_create(
                application=application,
                student=applicant.student,
                team=None
            )
        elif applicant.team:
            for member in applicant.team.students.all():
                Participant.objects.get_or_create(
                    application=application,
                    student=member,
                    team=applicant.team
                )
        return application

    def update(self, instance, validated_data):
        applicant_data = validated_data.pop('applicant', None)
        
        # Обновляем заявку
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем заявителя (если передан)
        if applicant_data and hasattr(instance, 'applicant'):
            applicant = instance.applicant
            for attr, value in applicant_data.items():
                setattr(applicant, attr, value)
            applicant.save()
        
        return instance
    
class TeamSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    students_ids = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True, write_only=True, source='students'
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'students', 'students_ids']

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        team = Team.objects.create(**validated_data)
        team.students.set(students)
        return team