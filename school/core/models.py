from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class StudentManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=User.TYPE_STUDENT,
        )


class TeacherManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=User.TYPE_TEACHER,
        )


class TeacherStudentRelation(models.Model):
    teacher = models.ForeignKey(
        'core.User',
        related_name='teacher_student_relations',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        'core.Student',
        related_name='student_teacher_relations',
        on_delete=models.CASCADE,
    )
    starred = models.BooleanField(_('starred'), default=False)

    def __str__(self):
        return f'{self.teacher.username} x {self.student.username}'

    class Meta:
        unique_together = ('teacher', 'student')


class User(AbstractUser):
    TYPE_STUDENT = 'student'
    TYPE_TEACHER = 'teacher'
    TYPE_CHOICES = (
        (TYPE_STUDENT, _('Student')),
        (TYPE_TEACHER, _('Teacher')),
    )

    type = models.CharField(
        _('type'),
        max_length=8,
        default=TYPE_STUDENT,
        db_index=True,
    )
    students = models.ManyToManyField(
        'core.Student',
        through='core.TeacherStudentRelation',
        through_fields=('teacher', 'student'),
        related_name='student_users',
        verbose_name=_('Students'),
        symmetrical=False,
        blank=True,
    )
    teachers = models.ManyToManyField(
        'core.Teacher',
        blank=True,
        related_name='teacher_users',
        verbose_name=_('Teachers'),
        symmetrical=False,
    )

    def __str__(self):
        return f'{self.username}'


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('teacher-detail', kwargs={'pk': self.pk})

    @property
    def relation_name(self):
        return 'students'

    @property
    def relation(self):
        return self.students.all()

    @property
    def not_related(self):
        return Student.objects.filter(
            ~Q(id__in=self.students.values_list('id')),
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.TYPE_TEACHER
        return super().save(*args, **kwargs)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    @property
    def relation_name(self):
        return 'teachers'

    @property
    def relation(self):
        return self.teachers.all()

    @property
    def not_related(self):
        return Teacher.objects.filter(
            ~Q(id__in=self.teachers.values_list('id')),
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.TYPE_STUDENT
        return super().save(*args, **kwargs)
