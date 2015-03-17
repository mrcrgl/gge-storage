from django import template
from django.template.base import Node

register = template.Library()

from django.conf import settings

DEPLOYMENT_ID = getattr(settings, "DEPLOYMENT_ID", '')


class DeploymentIdNode(Node):

    def render(self, context):
        return DEPLOYMENT_ID

    @classmethod
    def handle_token(cls, parser, token):
        return cls()


@register.tag('commit_id')
def deployment_id(parser, token):
    """
    Joins the given path with the STATIC_URL setting.

    Usage::

        {% static path [as varname] %}

    Examples::

        {% static "myapp/css/base.css" %}
        {% static variable_with_path %}
        {% static "myapp/css/base.css" as admin_base_css %}
        {% static variable_with_path as varname %}

    """
    return DeploymentIdNode.handle_token(parser, token)