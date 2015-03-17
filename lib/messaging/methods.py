from .template.loaders import load_template
from django.core.mail import EmailMessage
from django.conf import settings
import os


def send_message(slug, receiver, arguments={}, attachments=None):
    """
    Loads the message via slug, renders it with given arguments and sends to receiver.
    """
    message = load_template(slug)

    # TODO Implementation of internal messages should be done, too

    # TODO Delayed transfer via Celery (default option)

    # TODO Allow sending to User model and email address, maybe we decide there to transmit it internally or external.

    email = EmailMessage(
        subject=message.render_subject(arguments),
        body=message.render_content(arguments),
        to=[receiver],
        bcc=[message.bcc]
    )

    email.content_subtype = "html"

    for attachment in message.get_attachments():
        attachment_path = os.path.join(settings.MEDIA_ROOT, attachment)
        if os.path.isfile(attachment_path):
            print "Attach file: %s" % attachment_path
            email.attach_file(attachment_path)

    if attachments:
        for attachment in attachments:
            if os.path.isfile(attachment):
                print "Attach file2: %s" % attachment
                email.attach_file(attachment)

    try:
        email.send()
        return True
    except Exception, e:
        return e


def send_mass_message(slug, receivers, arguments={}):
    # TODO Implement mass messages
    pass