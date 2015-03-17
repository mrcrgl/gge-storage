from django import template

register = template.Library()


@register.tag()
def is_active(parser, token, class_name="active"):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1], class_name)


class NavSelectedNode(template.Node):
    def __init__(self, url, class_name):
        #print url
        self.url = url
        self.class_name = class_name

    def render(self, context):
        path = context['request'].path
        pValue = template.Variable(self.url).resolve(context)
        if (pValue == '/' or pValue == '') and not (path == '/' or path == ''):
            return ""
        if path.startswith(pValue):
            return " %s" % self.class_name
        return ""