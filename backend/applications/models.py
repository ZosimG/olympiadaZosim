from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Employee, Person
from olymp.models import Olympiada
from schools.models import School, Subdivision

# Create your models here.
pending = 0
accepted = 1
rejected = 2

APPLICATION_STATUS = ((pending, "В ожидании"), (accepted, "Принята"), (rejected, "Отклонена"))


male = 0
female = 1

sex = ((male, "Мужской"),(female, "Женский"))


class Country(models.Model):
    country_name = models.CharField("Название страны", max_length=200)

    def __str__(self):
        return self.country_name


class Student(Person):
    birthday = models.DateField("Дата рождения")
    course_study = models.IntegerField("Класс обучения", validators=[MinValueValidator(1), MaxValueValidator(12)])
    special_needs = models.BooleanField("Ограниченные возможности здоровья", default=False)
    contact_phone = models.CharField("Контактный номер телефона", max_length=20)
    country = models.ForeignKey(Country, verbose_name="Страна", null=True, on_delete=models.SET_NULL, related_name='countries')
    sex = models.IntegerField("Пол", choices=sex)

class Application(models.Model):
    student = models.ForeignKey(Student, verbose_name="Учащийся", on_delete=models.CASCADE, related_name='students')
    olymp = models.ForeignKey(Olympiada, verbose_name="Олимпиада", on_delete=models.CASCADE, related_name='olympiadas')
    date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    employee = models.ForeignKey(Employee, verbose_name="Ответственный", null=True, on_delete=models.SET_NULL, related_name='employees')
    status = models.IntegerField(default=0, verbose_name="Статус заявки", choices=APPLICATION_STATUS)
    participate = models.IntegerField("Класс участия", validators=[MinValueValidator(1), MaxValueValidator(12)])
    school = models.ForeignKey(School, verbose_name="Общеобразовательная организация", null=True, on_delete=models.SET_NULL, related_name='schools')
    teacher = models.ForeignKey(Employee, verbose_name="Учитель", null=True, on_delete=models.SET_NULL, related_name='teachers')
    subdivision = models.ForeignKey(Subdivision, verbose_name="Местоположение", null=True, on_delete=models.SET_NULL, related_name='app_subdivisions')
