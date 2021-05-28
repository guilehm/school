from django.db.models.signals import m2m_changed, pre_save, pre_delete
from django.dispatch import receiver

from school.core.models import Teacher, Student, TeacherStudentRelation


@receiver(pre_save, sender=TeacherStudentRelation)
def create_reverse_relation(sender, **kwargs):
    teacher = kwargs['instance'].teacher
    student = kwargs['instance'].student
    student.teachers.add(teacher.id)


@receiver(pre_delete, sender=TeacherStudentRelation)
def delete_reverse_relation(sender, **kwargs):
    teacher = kwargs['instance'].teacher
    student = kwargs['instance'].student
    student.teachers.remove(teacher.id)


@receiver(m2m_changed, sender=Student.teachers.through)
def update_student_relationship(sender, instance, **kwargs):
    student = instance
    teachers = Teacher.objects.filter(id__in=kwargs['pk_set'])
    for teacher in teachers:
        if 'add' in kwargs['action']:
            TeacherStudentRelation.objects.get_or_create(
                teacher=teacher,
                student=student,
            )
        elif 'remove' in kwargs['action']:
            TeacherStudentRelation.objects.filter(
                teacher=teacher,
                student=student,
            ).delete()
