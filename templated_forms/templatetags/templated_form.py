from django import template
register = template.Library()

from templated_forms.nodes import FormFactoryTemplateNode
from templated_forms.widgets import WidgetFactory


@register.tag
def parse_form(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return FormFactoryTemplateNode(form)


@register.filter
def parse_field(field):
    wf = WidgetFactory(field)
    return wf.get_widget().render()