from django import template

register = template.Library()


@register.inclusion_tag('core/tags/user-table.html')
def user_table(instances, col1, col2):
    return {
        'instances': instances,
        'col1': col1,
        'col2': col2,
    }


@register.inclusion_tag('core/tags/user-add-form.html')
def user_add_form(form, name):
    return {'form': form, 'name': name}
