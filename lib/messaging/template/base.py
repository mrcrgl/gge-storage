from django.template import Context


class MessageTemplate():

    subject = None
    bcc = None
    content = None
    attachments = []

    def __init__(self, subject, content, bcc=None):
        self.subject = subject
        self.bcc = bcc
        self.content = content
        self.attachments = []

    def render_subject(self, arguments={}):
        return self.render(self.subject, arguments)

    def render_content(self, arguments={}):
        return self.render(self.content, arguments)

    def render(self, template, arguments={}):
        return template.render(Context(arguments))

    def append_attachment(self, relative_path):
        self.attachments.append(relative_path)

    def get_attachments(self):
        return self.attachments