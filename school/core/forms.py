from django import forms

from school.core.models import Teacher, Student


class UserForm(forms.ModelForm):
    class Meta:
        fields = (
            'username',
            'password',
        )
        widgets = {
            'password': forms.PasswordInput(),
        }


class TeacherForm(UserForm):
    class Meta(UserForm.Meta):
        model = Teacher


class StudentForm(UserForm):
    class Meta(UserForm.Meta):
        model = Student
