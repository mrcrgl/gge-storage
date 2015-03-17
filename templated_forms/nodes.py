from django.template import Library, Node, Variable, loader
#from django.template.context import Context
from templated_forms.factory import FormFactory
from django import template


class FormFactoryTemplateNode(Node):
    def __init__(self, form):
        self.form = template.Variable(form)

    def render(self, context):
        form = self.form.resolve(context)
        self.factory = FormFactory(form)
        return self.factory.render()