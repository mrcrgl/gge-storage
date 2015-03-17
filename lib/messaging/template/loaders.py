from .backends import MESSAGING_BACKEND_CLASSES, get_backend
from django.template import TemplateDoesNotExist


def load_template(slug):
    # TODO Cache result? and if, here or at another place?
    for backend_class in MESSAGING_BACKEND_CLASSES:
        Backend = get_backend(backend_class)
        backend = Backend()
        try:
            return backend.get_template(slug)
        except TemplateDoesNotExist:
            pass

    raise TemplateDoesNotExist()