from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Olympiada(models.Model):
    olymp_name = models.CharField("Наименование", max_length=200, db_index=True)
    olymp_date_start = models.DateField("Дата проведения")
    olymp_time = models.TimeField("Длительность")
    
    
class Participant(models.Model):
    from applications.models import Application, Student
    student = models.ForeignKey(Student, verbose_name="Учащийся", on_delete=models.CASCADE, related_name='participant_students')
    application = models.ForeignKey(Application, verbose_name="Заявка", on_delete=models.CASCADE, related_name='participant_applications')
    


class Result(models.Model):
    participant = models.ForeignKey("Participant", verbose_name="Участник", on_delete=models.CASCADE, related_name='result_students')
    task_number = models.CharField("Номер задачи", max_length=1)
    result_value = models.IntegerField(verbose_name="Балл", validators=[MinValueValidator(0), MaxValueValidator(100)])
    














