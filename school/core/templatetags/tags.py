from django import template

register = template.Library()


@register.inclusion_tag('core/tags/user-table-tag.html')
def user_table(instances, col1, col2):
    return {
        'instances': instances,
        'col1': col1,
        'col2': col2,
    }


@register.inclusion_tag('core/tags/user-change-form-tag.html')
def user_change_form(form, name, method=None):
    return {'form': form, 'name': name, 'method': method}
