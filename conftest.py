import pytest

from school.core.models import Student, Teacher, TeacherStudentRelation


@pytest.fixture
def student():
    return Student.objects.create(
        username='frodo',
    )


@pytest.fixture
def teacher():
    return Teacher.objects.create(
        username='gandalf',
    )


@pytest.fixture
def relation(student, teacher):
    return TeacherStudentRelation.objects.create(
        teacher=teacher,
        student=student,
        starred=False,
    )
