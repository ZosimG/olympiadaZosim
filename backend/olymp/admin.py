from django.contrib import admin
from users.models import Person, Employee
from schools.models import Subdivision, School
from .models import Olympiada
from applications.models import Application, Student, Country

# Register your models here.
admin.site.register(Olympiada)
admin.site.register(Person)
admin.site.register(Employee)
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(Subdivision)
admin.site.register(School)
admin.site.register(Country)
