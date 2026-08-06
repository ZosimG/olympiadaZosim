from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from users.models import Employee, Person
from schools.models import School, Subdivision

# Create your models here.
pending = 0
accepted = 1
rejected = 2

APPLICATION_STATUS = ((pending, "В ожидании"), (accepted, "Принята"), (rejected, "Отклонена"))

male = 0
female = 1

sex = ((male, "Мужской"), (female, "Женский"))

individual = 0
team = 1


individual = 0
team = 1

OLYMPIADA_TYPE = ((individual, "Индивидуальная"),
                  (team, "Командная"))


class Country(models.Model):
    country_name = models.CharField("Название страны", max_length=200)

    def __str__(self):
        return self.country_name


class Student(Person):
    birthday = models.DateField("Дата рождения")
    course_study = models.IntegerField("Класс обучения", validators=[MinValueValidator(1), MaxValueValidator(12)])
    special_needs = models.BooleanField("Ограниченные возможности здоровья", default=False)
    contact_phone = models.CharField("Контактный номер телефона", max_length=20)
    country = models.ForeignKey(Country, verbose_name="Страна", null=True, on_delete=models.SET_NULL, related_name='students')
    sex = models.IntegerField("Пол", choices=sex)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Team(models.Model):
    name = models.CharField("Название команды", max_length=200)
    students = models.ManyToManyField(Student, verbose_name="Участники", related_name='teams')

    def __str__(self):
        return self.name


class Application(models.Model):
    olymp = models.ForeignKey('olymp.Olympiada', verbose_name="Олимпиада", on_delete=models.CASCADE, related_name='applications')
    date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    employee = models.ForeignKey(Employee, verbose_name="Ответственный", null=True, on_delete=models.SET_NULL, related_name='applications')
    status = models.IntegerField(default=0, verbose_name="Статус заявки", choices=APPLICATION_STATUS)
    participate = models.IntegerField("Класс участия", validators=[MinValueValidator(1), MaxValueValidator(12)])
    school = models.ForeignKey(School, verbose_name="Общеобразовательная организация", null=True, on_delete=models.SET_NULL, related_name='applications')
    teacher = models.ForeignKey(Employee, verbose_name="Учитель", null=True, on_delete=models.SET_NULL, related_name='teaching_applications')
    subdivision = models.ForeignKey(Subdivision, verbose_name="Местоположение", null=True, on_delete=models.SET_NULL, related_name='applications')
    participation_type = models.IntegerField("Тип участия", choices=OLYMPIADA_TYPE, default=individual)

    def __str__(self):
        applicant = self.applicant
        if applicant and applicant.student:
            return f"Заявка {applicant.student.last_name} на {self.olymp.olymp_name}"
        elif applicant and applicant.team:
            return f"Заявка команды {applicant.team.name} на {self.olymp.olymp_name}"
        return f"Заявка #{self.id} на {self.olymp.olymp_name}"


class Applicant(models.Model):
    application = models.OneToOneField(Application, verbose_name="Заявка", on_delete=models.CASCADE, related_name='applicant')
    student = models.ForeignKey(Student, verbose_name="Студент (индивидуально)", on_delete=models.CASCADE, null=True, blank=True, related_name='applications_as_student')
    team = models.ForeignKey(Team, verbose_name="Команда", on_delete=models.CASCADE, null=True, blank=True, related_name='applications_as_team')

    class Meta:
        verbose_name = "Заявитель"
        verbose_name_plural = "Заявители"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(student__isnull=False, team__isnull=True) |
                    models.Q(student__isnull=True, team__isnull=False)
                ),
                name="applicant_student_or_team_not_both"
            )
        ]

    def clean(self):
        if not self.student and not self.team:
            raise ValidationError("Должен быть указан либо студент, либо команда")
        
        if self.student and self.team:
            raise ValidationError("Нельзя указать и студента, и команду одновременно")
        
        # Проверка соответствия типу участия в заявке
        if self.application.participation_type == individual:
            if not self.student:
                raise ValidationError({'student': 'Для индивидуальной заявки необходимо указать студента'})
            if self.team:
                raise ValidationError({'team': 'Для индивидуальной заявки команда не указывается'})
        elif self.application.participation_type == team:
            if not self.team:
                raise ValidationError({'team': 'Для командной заявки необходимо указать команду'})
            if self.student:
                raise ValidationError({'student': 'Для командной заявки студент указывается через команду'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.student:
            return f"{self.student} → {self.application}"
        else:
            return f"{self.team} → {self.application}"

    @property
    def all_participants(self):
        """Возвращает список всех участников (студентов) по заявке"""
        if self.student:
            return [self.student]
        elif self.team:
            return list(self.team.students.all())
        return []