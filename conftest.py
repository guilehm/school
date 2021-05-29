import pytest

from school.core.models import Student, Teacher


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
