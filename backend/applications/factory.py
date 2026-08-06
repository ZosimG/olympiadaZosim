from django.db.models.expressions import result

import datetime
from schools.models import Subdivision, School
from users.models import Employee, Person, ROLES
from applications.models import Student, Country, Application
from olymp.models import Olympiada
from schools.factory import Factory

class Factory:

    @classmethod
    def create_application(cls, data_array, olympiada, employee):
        result = ""
        student_name = cls.get_student_name(data_array)
        print("Got Student Name")
        student = cls.get_student(data_array, student_name)
        if student is None:
            result += "Студент " + student_name + " не был создан или найден \n"
            return result
        print("Got Student")
        subdivision, result = cls.get_subdivision(data_array, student_name, result)
        if subdivision is None:
            return result
        print("Got Subdivision")
        school, result = cls.get_school(data_array, subdivision, student_name, result)
        print("Got School")
        teacher, created = Employee.objects.get_or_create(
            name=data_array[12].value, 
            role=ROLES[2][0]
        )
        print("Got Teacher")
        if created:
            result += "Для студента " + student_name + " добавлен новый учитель " + data_array[12].value + "\n"
        participate = data_array[11].value
        print("Got participate class")
        try:
            application = Application.objects.create(
                olymp=olympiada,
                employee=employee,
                participate=participate,
                school=school,
                teacher=teacher,
                subdivision=subdivision
            )
            Applicant.objects.create(
                application=application,
                student=student,
                team=None
            )
            result += "Заявка студента " + student_name + " успешно добавлена\n"
        except Exception as e:
            print(e)
            result += "Ошибка при добавлении заявки студента " + student_name + "\n"
        return result

    @classmethod
    def get_student_name(cls, data_array):
        student_name = data_array[1].value + " " + data_array[2].value
        if data_array[3].value is not None:
            student_name += " " + data_array[3].value
        return student_name

    @classmethod
    def get_student(cls, data_array, student_name):
        sex = 0 if 'м' in data_array[4].value.lower() else 1
        print("Got Sex")
        birthday = data_array[5].value
        if isinstance(birthday, datetime.datetime):
            birthday = birthday.date()
        elif isinstance(birthday, str):
            birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y").date()
        print("Got Birthday")
        try:
            country = Country.objects.get(country_name=data_array[6].value)
        except Country.DoesNotExist:
            return None
        student, created = Student.objects.get_or_create(
            name=student_name,
            sex=sex,
            birthday=birthday,
            defaults={
                "course_study": data_array[11].value,
                "special_needs": 'не' not in data_array[7].value.lower(),
                "contact_phone": data_array[13].value,
                "country": country
            }
        )
        return student

    @classmethod
    def get_subdivision(cls, data_array, student_name, result):
        try:
            subdivision = Subdivision.objects.get(
                subdivision_name__icontains=data_array[8].value.split()[0]
            )
            return subdivision, result
        except Subdivision.DoesNotExist:
            result += "Муниципалитет для студента " + student_name + " не найден\n"
            return None, result

    @classmethod
    def get_school(cls, data_array, subdivision, student_name, result):
        try:
            school = School.objects.get(
                school_name=data_array[9].value, 
                school_subdivision=subdivision
            )
            return school, result
        except School.DoesNotExist:
            result += "Школа для студента " + student_name + " не найдена\n"
            return None, result


class TeamApplicationFactory:

    @classmethod
    def create_team_application(cls, team_data, olympiada, employee):
        result = ""
        team, created = Team.objects.get_or_create(
            name=team_data['team_name']
        )
        if created:
            result += f"Создана новая команда: {team.name}\n"
        for student in team_data['members']:
            team.students.add(student)
        try:
            application = Application.objects.create(
                olymp=olympiada,
                employee=employee,
                participate=team_data['participate'],
                school=team_data['school'],
                teacher=team_data['teacher'],
                subdivision=team_data['subdivision']
            )
            Applicant.objects.create(
                application=application,
                student=None,
                team=team
            )
            result += f"Командная заявка для команды {team.name} успешно добавлена\n"
        except Exception as e:
            print(e)
            result += f"Ошибка при добавлении командной заявки: {team.name}\n"
        return result