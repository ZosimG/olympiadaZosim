from django.db.models.expressions import result

import datetime
from schools.models import Subdivision, School
from users.models import Employee, Person, ROLES
from applications.models import Student, Country, Application
from olymp.models import Olympiada


class Factory():
    @classmethod
    def create_school(cls, school_name, subdivision_name):
        result = ""
        sd = Subdivision.objects.filter(subdivision_name__icontains=subdivision_name).first()
        if sd is not None:
            school = School()
            school.school_name = school_name
            school.school_subdivision = sd
            school.save()
        else:
            result += "Для школы " + school_name + " не найдено Муниципальное Образование " + subdivision_name + "\n"
        return result


    @classmethod
    def get_school(cls, data_array, subdivision, student_name, result):
        # print(data_array[9].value)
        # print(subdivision.subdivision_name)
        school = School.objects.filter(school_subdivision__id=subdivision.id, school_name__icontains=data_array[9].value).first()
        if school is None:
            cls.create_school(data_array[9].value, subdivision.subdivision_name)
            result += "Для студента " + student_name + " добавлена новая школа " + data_array[9].value + "\n"
        return school, result

    @classmethod
    def get_subdivision(cls, data_array, student_name, result):
        subdivision = Subdivision.objects.filter(subdivision_name__icontains=data_array[8].value).first()
        if subdivision is None:
            result += "Для студента " + student_name + " не указано муниципальное образование \n"
        return subdivision, result

    @classmethod
    def create_subdivision(cls, subdivision_name):
        result = ""
        sd = Subdivision.objects.filter(subdivision_name__icontains=subdivision_name).first()
        if sd is None:
            subdivision = Subdivision()
            subdivision.subdivision_name = subdivision_name
            subdivision.save()
        else:
            result += "Муниципальное образование " + subdivision_name + " уже существует.\n"
        return result
