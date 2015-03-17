from templated_forms.widgets import WidgetFactory


class FormFactory(object):
    instance = None

    def __init__(self, instance):
        self.instance = instance

    def render(self):
        return "%s%s" % (self.render_hidden_fields(), self.render_visible_fields())

    def render_hidden_fields(self):
        html = ""

        for hidden_field in self.instance.hidden_fields():
            html += str(hidden_field)

        return html

    def render_visible_fields(self):
        html = ""

        for visible_field in self.instance.visible_fields():
            try:
                wf = WidgetFactory(visible_field)
                html += wf.get_widget().render()
            except NotImplementedError:
                html += visible_field.__str__()

        return html