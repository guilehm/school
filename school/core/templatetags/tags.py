from django import template

from school.core.models import TeacherStudentRelation

register = template.Library()


@register.inclusion_tag('core/tags/user-table-tag.html')
def user_table(instances, col1, col2=None, instance=None):
    return {
        'instance': instance,
        'instances': instances,
        'col1': col1,
        'col2': col2,
    }


@register.inclusion_tag('core/tags/user-available-table-tag.html')
def user_available_table(instances, instance=None):
    return {
        'instance': instance,
        'instances': instances,
    }


@register.inclusion_tag('core/tags/user-change-form-tag.html')
def user_change_form(form, name, method=None):
    return {'form': form, 'name': name, 'method': method}


@register.filter
def is_starred(teacher, student):
    try:
        return TeacherStudentRelation.objects.get(
            teacher=teacher,
            student=student,
        ).starred
    except TeacherStudentRelation.DoesNotExist:
        return False
