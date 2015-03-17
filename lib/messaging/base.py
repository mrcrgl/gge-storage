from .tasks import send_message as send_message_task


def send_message(slug, receiver, arguments={}, attachments=None):
    send_message_task.delay(slug, receiver, arguments, attachments)


def send_mass_message(slug, receivers, arguments={}):
    # TODO Implement mass messages
    pass