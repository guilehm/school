import graphene
from graphene_django import DjangoObjectType

from school.core.models import Teacher, Student


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = (
            'id',
            'username',
            'date_joined',
            'last_login',
        )


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = (
            'id',
            'username',
            'date_joined',
            'last_login',
        )


class Query(graphene.ObjectType):
    all_teachers = graphene.List(TeacherType)
    all_students = graphene.List(StudentType)

    teacher_by_username = graphene.Field(
        TeacherType, username=graphene.String(required=True)
    )
    student_by_username = graphene.Field(
        StudentType, username=graphene.String(required=True)
    )

    def resolve_all_teachers(root, info):
        return Teacher.objects.all()

    def resolve_all_students(root, info):
        return Student.objects.all()

    def resolve_teacher_by_username(root, info, username):
        try:
            return Teacher.objects.get(username=username)
        except Teacher.DoesNotExist:
            return None

    def resolve_student_by_username(root, info, username):
        try:
            return Student.objects.get(username=username)
        except Student.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
