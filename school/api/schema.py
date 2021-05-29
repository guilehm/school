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

    def resolve_all_teachers(root, info):
        return Teacher.objects.all()

    def resolve_all_students(root, info):
        return Student.objects.all()


schema = graphene.Schema(query=Query)
