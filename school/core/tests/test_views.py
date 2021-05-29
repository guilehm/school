import pytest
from django.urls import reverse

from school.core.models import TeacherStudentRelation


@pytest.mark.django_db
class TestViews:

    @pytest.fixture
    def star_relation_url(self):
        return reverse('stars')

    @pytest.fixture
    def relation_creation_url(self):
        return reverse('relations')

    def test_should_return_200_for_teacher_and_student_list_endpoints(self, client):
        teacher_list_url = reverse('teacher-list')
        student_list_url = reverse('student-list')

        teacher_list_response = client.get(teacher_list_url)
        student_list_response = client.get(student_list_url)

        assert teacher_list_response.status_code == 200
        assert student_list_response.status_code == 200

    def test_should_return_200_for_teacher_and_student_detail_endpoints(
            self, client, teacher, student
    ):
        teacher_list_url = reverse('teacher-detail', kwargs={'pk': teacher.pk})
        student_list_url = reverse('student-detail', kwargs={'pk': student.pk})

        teacher_detail_response = client.get(teacher_list_url)
        student_detail_response = client.get(student_list_url)

        assert teacher_detail_response.status_code == 200
        assert student_detail_response.status_code == 200

    def test_should_not_accept_other_methods_than_post_in_star_relation_endpoint(
            self, client, star_relation_url
    ):
        response = client.get(star_relation_url)
        assert response.status_code == 405

    def test_should_return_bad_request_for_wrong_payload_in_star_relation_endpoint(
            self, client, star_relation_url, relation
    ):
        response = client.post(
            star_relation_url,
            data={'wrong': 'payload'},
            content_type='application/json',
        )
        assert response.status_code == 400

    def test_should_return_bad_request_if_relation_does_not_exists_in_star_relation_endpoint(
            self, client, star_relation_url, teacher, student
    ):
        response = client.post(
            star_relation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )
        assert response.status_code == 400

    def test_should_return_200_for_correct_payload_in_star_relation_endpoint(
            self, client, star_relation_url, teacher, student, relation
    ):
        response = client.post(
            star_relation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_should_set_starred_relation_in_star_relation_endpoint(
            self, client, star_relation_url, teacher, student, relation
    ):
        assert relation.starred is False

        client.post(
            star_relation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )

        relation.refresh_from_db()
        assert relation.starred is True

    def test_should_not_accept_other_methods_than_post_in_relation_creation_endpoint(
            self, client, relation_creation_url
    ):
        response = client.get(relation_creation_url)
        assert response.status_code == 405

    def test_should_return_bad_request_for_wrong_payload_in_relation_creation_endpoint(
            self, client, relation_creation_url
    ):
        response = client.post(
            relation_creation_url,
            data={'wrong': 'payload'},
            content_type='application/json',
        )
        assert response.status_code == 400

    def test_should_create_relation_in_relation_creation_endpoint(
            self, client, relation_creation_url, teacher, student
    ):
        assert teacher not in student.teachers.all()
        assert student not in teacher.students.all()

        response = client.post(
            relation_creation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )
        assert response.status_code == 200

        assert teacher in student.teachers.all()
        assert student in teacher.students.all()
