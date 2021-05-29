import graphene
from graphene_django import DjangoObjectType

from school.core.models import Student, Teacher, TeacherStudentRelation


class TeacherStudentRelationType(DjangoObjectType):
    id = graphene.ID()
    username = graphene.String()

    class Meta:
        model = TeacherStudentRelation
        fields = (
            'starred',
        )

    def resolve_id(self, info):
        return self.student.id

    def resolve_username(self, info):
        return self.student.username


class StudentType(DjangoObjectType):
    teachers = graphene.List(lambda: TeacherType)

    class Meta:
        model = Student
        fields = (
            'id',
            'username',
            'date_joined',
            'last_login',
        )

    def resolve_teachers(self, info):
        return self.teachers.all()


class TeacherType(DjangoObjectType):
    students = graphene.List(TeacherStudentRelationType)

    class Meta:
        model = Teacher
        fields = (
            'id',
            'username',
            'date_joined',
            'last_login',
            'students',
        )

    def resolve_students(self, info):
        return TeacherStudentRelation.objects.filter(
            teacher=self,
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

    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    def resolve_all_students(self, info):
        return Student.objects.all()

    def resolve_teacher_by_username(self, info, username):
        try:
            return Teacher.objects.get(username=username)
        except Teacher.DoesNotExist:
            return None

    def resolve_student_by_username(self, info, username):
        try:
            return Student.objects.get(username=username)
        except Student.DoesNotExist:
            return None


class TeacherStudentRelationMutation(graphene.Mutation):
    class Arguments:
        teacher_id = graphene.ID()
        student_id = graphene.ID()

    relation = graphene.Field(TeacherStudentRelationType)

    @classmethod
    def mutate(cls, root, info, teacher_id, student_id):
        relation = TeacherStudentRelation.objects.get(
            teacher_id=teacher_id,
            student_id=student_id,
        )
        relation.starred = not relation.starred
        relation.save(update_fields=('starred',))
        return TeacherStudentRelationMutation(relation=relation)


class Mutation(graphene.ObjectType):
    toggle_starred = TeacherStudentRelationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
