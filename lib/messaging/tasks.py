from .methods import send_message as send_message_original
import celery


@celery.task
def send_message(*args, **kwargs):
    return send_message_original(*args, **kwargs)