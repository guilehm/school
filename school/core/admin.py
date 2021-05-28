from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from school.core.models import Student, Teacher

base_user_fieldsets = (
    (None, {'fields': ('username', 'password')}),
    (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser',),
    }),
    (_('Important dates'), {'fields': ('last_login',)}),
)


class TeacherStudentRelationInline(admin.TabularInline):
    model = Teacher.students.through
    raw_id_fields = ('student',)
    extra = 0


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    exclude = ('type',)
    fieldsets = (
        *base_user_fieldsets,
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    filter_horizontal = ('user_permissions', 'students')
    inlines = (
        TeacherStudentRelationInline,
    )


@admin.register(Student)
class StudentAdmin(UserAdmin):
    exclude = ('type',)
    fieldsets = (
        *base_user_fieldsets,
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'teachers')}),
    )
    filter_horizontal = ('user_permissions', 'teachers')
