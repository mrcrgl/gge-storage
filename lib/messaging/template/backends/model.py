from lib.messaging.template.backends.object import DefaultMessagingTemplateBackend
from lib.messaging.models import Template as TemplateModel
from django.template import Template, TemplateDoesNotExist
from lib.messaging.template import MessageTemplate


class ModelMessagingTemplateBackend(DefaultMessagingTemplateBackend):

    def get_template(self, slug):
        template = self.fetch_message(slug)

        message = MessageTemplate(subject=Template(template.subject),
                                  bcc=template.always_bcc_to,
                                  content=Template(template.template))

        for attachment in template.attachments.all():
            print "Added file to MessageTemplate: %s" % attachment.file.path
            message.append_attachment(attachment.file.path)

        return message

    def fetch_message(self, slug):
        try:
            template = TemplateModel.objects.get(slug=slug)
        except TemplateModel.DoesNotExist:
            raise TemplateDoesNotExist()

        return template