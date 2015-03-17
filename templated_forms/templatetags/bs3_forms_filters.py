__author__ = 'mriegel'

from django import template
register = template.Library()


def unbound(form_field_obj):
    if form_field_obj.__class__.__name__ == "BoundField":
        return form_field_obj.field
    return form_field_obj


@register.filter
def is_checkbox_multi_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "CheckboxSelectMultiple"


@register.filter
def is_model_choice_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "ModelChoiceField"


@register.filter
def is_char_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "CharField"


@register.filter
def is_integer_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "IntegerField"


@register.filter
def is_float_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "FloatField"


@register.filter
def is_boolean_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "BooleanField"


@register.filter
def is_datetime_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "DateTimeField"


@register.filter
def is_date_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "DateField"


@register.filter
def is_text_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "TextField"


@register.filter
def is_typed_choice_field(form_field_obj):
    return unbound(form_field_obj).__class__.__name__ == "TypedChoiceField"


@register.filter
def get_widget(form_field_obj):
    return unbound(form_field_obj).__class__.__name__