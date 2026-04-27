from django.db import models
from django.contrib.auth.models import User


organizer = 0
representative = 1
teacher = 2

ROLES = ((organizer, "Организатор"),
        (representative, "Представитель муниципалитета"),
        (teacher, "Учитель"))


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200)
    #sex = models.CharField(max_length=200)
    #city = models.CharField(max_length=200)
    #munic_entity = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

class Employee(Person):
    role = models.IntegerField(default=0, choices=ROLES)
    user = models.ForeignKey(User, verbose_name="Пользователь", null=True, on_delete=models.CASCADE)