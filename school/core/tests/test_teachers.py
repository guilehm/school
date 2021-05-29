import pytest
from django.db import IntegrityError

from school.core.models import Teacher, User, TeacherStudentRelation


@pytest.mark.django_db
class TestTeacherCreation:

    def test_should_create_user_instance_for_teachers(self):
        assert User.objects.exists() is False
        Teacher.objects.create(
            username='bombadil',
        )
        assert User.objects.exists() is True

    def test_should_associate_correct_type_for_teachers(self):
        teacher = Teacher.objects.create(
            username='bombadil',
        )
        assert teacher.type == User.TYPE_TEACHER

    def test_should_recognize_teacher_proxy_by_type(self):
        assert Teacher.objects.exists() is False

        assert User.objects.create(username='aragorn', type=User.TYPE_STUDENT)
        assert Teacher.objects.exists() is False

        assert User.objects.create(username='legolas', type=User.TYPE_TEACHER)
        assert Teacher.objects.exists() is True


@pytest.mark.django_db
class TestStudentRelations:

    def test_should_associate_teachers_to_users(self, student, teacher):
        assert teacher.students.exists() is False
        TeacherStudentRelation.objects.create(
            teacher=teacher,
            student=student,
        )
        assert teacher.students.exists() is True

    def test_should_create_reverse_association_adding_teachers_to_students(
            self, student, teacher
    ):
        assert student.teachers.exists() is False
        TeacherStudentRelation.objects.create(
            teacher=teacher,
            student=student,
        )
        assert student.teachers.exists() is True

    def test_should_set_starred_default_as_false_for_relation(self, student, teacher):
        relation = TeacherStudentRelation.objects.create(
            teacher=teacher,
            student=student,
        )
        assert relation.starred is False

    def test_should_not_allow_multiple_relations_for_same_teacher_and_student(
            self, student, teacher,
    ):
        TeacherStudentRelation.objects.create(
            teacher=teacher,
            student=student,
        )
        with pytest.raises(IntegrityError):
            TeacherStudentRelation.objects.create(
                teacher=teacher,
                student=student,
            )

    def test_should_remove_reverse_relation(self, relation):
        student = relation.student
        teacher = relation.teacher

        assert TeacherStudentRelation.objects.exists() is True

        assert teacher in student.teachers.all()
        assert student in teacher.students.all()

        student.teachers.remove(teacher)

        assert teacher not in student.teachers.all()
        assert student not in teacher.students.all()

        assert TeacherStudentRelation.objects.exists() is False
