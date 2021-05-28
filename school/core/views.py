from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from school.core.forms import TeacherForm, StudentForm, TeacherChangeForm
from school.core.models import Teacher, Student


def index(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    changed_form = request.GET.get('type', '')
    teacher_form_has_changed = Teacher.TYPE_TEACHER in changed_form
    student_form_has_changed = Student.TYPE_STUDENT in changed_form
    teacher_form = TeacherForm(teacher_form_has_changed and request.POST or None)
    student_form = StudentForm(student_form_has_changed and request.POST or None)

    if request.method == 'POST':
        if teacher_form_has_changed and teacher_form.is_valid():
            teacher_form.save()
            messages.add_message(request, messages.SUCCESS, 'Teacher successfully created.')
            return redirect('index')
        if student_form_has_changed and student_form.is_valid():
            student_form.save()
            messages.add_message(request, messages.SUCCESS, 'Student successfully created.')
            return redirect('index')

    return render(request, 'core/index.html', {
        'teachers': teachers,
        'students': students,
        'teacher_form': teacher_form,
        'student_form': student_form,
    })


def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'core/user-list.html', {
        'instances': teachers,
        'name': 'teachers',
        'relation_name': 'students',
    })


def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherChangeForm(instance=teacher, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Success updating teacher.')
        return redirect('teacher-detail', pk=pk)

    return render(request, 'core/user-detail.html', {
        'instance': teacher,
        'form': form,
        'name': 'teacher',
        'method': 'update',
    })
