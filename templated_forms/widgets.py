from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import *
from lib.core.utils import load_class


class AbstractWidget(object):
    field_instance = None
    arguments = {}
    context = None

    def __init__(self, field, arguments=None, context=None):
        self.field_instance = field
        self.arguments = arguments or {}
        self.context = context or None

    def render(self):
        try:
            if getattr(self, "extra_arguments"):
                for key in getattr(self, "extra_arguments"):
                    self.arguments[key] = self.extra_arguments[key]
        except AttributeError:
            pass
        
        self.arguments['field'] = self.field_instance
        self.arguments['widget'] = self
        return render_to_string(self.template_name, self.arguments, self.context)


class TextInputWidget(AbstractWidget):
    template_name = 'templated_forms/widget/text_input.html'
    type = "text"


class EmailInputWidget(TextInputWidget):
    type = "email"


class NumberInputWidget(TextInputWidget):
    type = "text"


class PasswordInputWidget(TextInputWidget):
    type = "password"


class URLInputWidget(TextInputWidget):
    type = 'url'


class DisabledWidget(TextInputWidget):
    extra_arguments = {
        'disabled': True
    }


class CheckboxInputWidget(AbstractWidget):
    template_name = 'templated_forms/widget/checkbox_field.html'


class DateTimeInputWidget(AbstractWidget):
    template_name = 'templated_forms/widget/datetime_field.html'
    mode = "datetime"
    

class DateInputWidget(AbstractWidget):
    template_name = 'templated_forms/widget/datepicker_field.html'
    mode = "date"


class SelectWidget(AbstractWidget):
    template_name = 'templated_forms/widget/select.html'


class SelectMultipleWidget(SelectWidget):
    extra_arguments = {
        'multiple': True
    }


class TextareaWidget(AbstractWidget):
    template_name = 'templated_forms/widget/textarea.html'


class RichTextareaWidget(TextareaWidget):
    template_name = 'templated_forms/widget/textarea.html'
    extra_arguments = { 'classname' : 'toWysiwyg' }


class ClearableFileInputWidget(AbstractWidget):
    template_name = 'templated_forms/widget/clearable_file_input.html'


class HoneyPot(TextInputWidget):
    style = "display:none;"


class WidgetFactory(object):

    field_instance = None

    def __init__(self, field_instance):
        self.field_instance = field_instance

    def unbound(self):
        if self.field_instance.__class__.__name__ == "BoundField":
            return self.field_instance.field
        return self.field_instance

    def get_widget_class(self):
        return self.unbound().widget.__class__.__name__

    def get_widget(self):
        class_name = "".join((self.get_widget_class(), "Widget"))

        try:
            Widget = load_class(".".join((__name__, class_name)))
        except AttributeError:
            raise NotImplementedError("Widget of type %s is not implemented." % class_name)
            #return self.unbound().widget

        widget = Widget(self.field_instance)

        return widget
