from django.db import models


# Create your models here.
class Subdivision(models.Model):
    subdivision_name = models.CharField("Наименование района", max_length=200, db_index=True)

    def __str__(self):
        return self.subdivision_name


class School(models.Model):
    school_name = models.CharField("Название образовательной организации", max_length=200)
    school_subdivision = models.ForeignKey(Subdivision, verbose_name="Местоположение", null=True, on_delete=models.SET_NULL, related_name='subdivisions')

    def __str__(self):
        return self.school_name