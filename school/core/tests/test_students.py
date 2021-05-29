import pytest

from school.core.models import Student, User


@pytest.mark.django_db
class TestStudentCreation:

    def test_should_create_user_instance_for_students(self):
        assert User.objects.exists() is False
        Student.objects.create(
            username='legolas',
        )
        assert User.objects.exists() is True

    def test_should_associate_correct_type_for_students(self):
        student = Student.objects.create(
            username='legolas',
        )
        assert student.type == User.TYPE_STUDENT

    def test_should_recognize_student_proxy_by_type(self):
        assert Student.objects.exists() is False

        assert User.objects.create(username='bombadil', type=User.TYPE_TEACHER)
        assert Student.objects.exists() is False

        assert User.objects.create(username='aragorn', type=User.TYPE_STUDENT)
        assert Student.objects.exists() is True


@pytest.mark.django_db
class TestStudentRelations:

    def test_should_associate_teachers_to_users(self, student, teacher):
        assert student.teachers.exists() is False
        student.teachers.add(teacher)
        assert student.teachers.exists() is True

    def test_should_create_reverse_association_adding_teachers_to_users(
            self, student, teacher
    ):
        assert teacher.students.exists() is False
        student.teachers.add(teacher)
        assert teacher.students.exists() is True
