from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    try:
        return field.as_widget(attrs={
            **field.field.widget.attrs,
            "class": css_class
        })
    except AttributeError:
        # If it’s a SafeString, just return it unchanged
        return field
