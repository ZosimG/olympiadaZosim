from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.models import Application, Student, Team
# Create your models here.

programming = 0
robots = 1
security = 2
Ai = 3

OLYMPIADA_SPECIALIZATION = ((programming, "Программирование"),
                            (robots, "Робототехника"),
                            (security, "Информационная безопасность"),
                            (Ai, "Искусственный интеллект"))

individual = 0
team = 1

OLYMPIADA_TYPE = ((individual, "Индивидуальная"),
                  (team, "Командная"))


class Olympiada(models.Model):
    olymp_name = models.CharField("Наименование", max_length=200, db_index=True)
    olymp_date_start = models.DateField("Дата проведения")
    olymp_time = models.TimeField("Длительность")
    olymp_type = models.IntegerField(default=0, verbose_name="Тип олимпиады", choices=OLYMPIADA_TYPE)
    olymp_specialization = models.IntegerField(default=0, verbose_name="Специализация олимпиады", choices=OLYMPIADA_SPECIALIZATION)
    
class Participant(models.Model):
    application = models.ForeignKey(Application, verbose_name="Заявка", on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(Student, verbose_name="Участник", on_delete=models.CASCADE, related_name='participants')
    team = models.ForeignKey(Team, verbose_name="Команда", on_delete=models.SET_NULL, null=True, blank=True, related_name='participants')

    class Meta:
        unique_together = [['application', 'student']]
        ordering = ['application', 'student__name']
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def clean(self):
        if self.application.participation_type == team:
            if not self.team:
                raise ValidationError({'team': 'Для командной заявки необходимо указать команду'})
            if self.student not in self.team.students.all():
                raise ValidationError({'student': f'Студент {self.student} не состоит в команде {self.team}'})
        elif self.application.participation_type == individual:
            if self.team:
                raise ValidationError({'team': 'Для индивидуальной заявки команда не указывается'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.application.participation_type == individual:
            return f"{self.student} - {self.application.olymp.olymp_name}"
        else:
            return f"{self.student} (команда: {self.team.name}) - {self.application.olymp.olymp_name}"


class Result(models.Model):
    participant = models.ForeignKey(Participant, verbose_name="Участник", on_delete=models.CASCADE, related_name='results')
    task_number = models.CharField("Номер задачи", max_length=1)
    result_value = models.IntegerField("Балл", validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.participant.student} - Задача {self.task_number}: {self.result_value}"
    














