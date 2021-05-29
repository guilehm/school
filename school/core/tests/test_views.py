import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestViews:

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
            self, client,
    ):
        star_relation_url = reverse('stars')
        response = client.get(star_relation_url)
        assert response.status_code == 405

    def test_should_return_bad_request_for_wrong_payload_in_star_relation_endpoint(
            self, client, relation
    ):
        star_relation_url = reverse('stars')
        response = client.post(
            star_relation_url,
            data={'wrong': 'payload'},
            content_type='application/json',
        )
        assert response.status_code == 400

    def test_should_return_bad_request_if_relation_does_not_exists_in_star_relation_endpoint(
            self, client, teacher, student
    ):
        star_relation_url = reverse('stars')
        response = client.post(
            star_relation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )
        assert response.status_code == 400

    def test_should_return_200_for_correct_payload_in_star_relation_endpoint(
            self, client, teacher, student, relation
    ):
        star_relation_url = reverse('stars')
        response = client.post(
            star_relation_url,
            data={'teacher': teacher.id, 'student': student.id},
            content_type='application/json',
        )
        assert response.status_code == 200
