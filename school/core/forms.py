from django import forms
from django.contrib.auth.hashers import make_password

from school.core.models import Student, Teacher


class UserForm(forms.ModelForm):
    class Meta:
        fields = (
            'username',
            'password',
        )
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        return make_password(self.cleaned_data['password'])


class TeacherForm(UserForm):
    class Meta(UserForm.Meta):
        model = Teacher


class StudentForm(UserForm):
    class Meta(UserForm.Meta):
        model = Student


class TeacherChangeForm(TeacherForm):
    class Meta(TeacherForm.Meta):
        fields = (
            'username',
        )


class StudentChangeForm(StudentForm):
    class Meta(StudentForm.Meta):
        fields = (
            'username',
        )
