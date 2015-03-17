from lib.core.utils import load_class

MESSAGING_BACKEND_CLASSES = (
    'lib.messaging.template.backends.model.ModelMessagingTemplateBackend',
    #'libs.messaging.template.backends.file.FileMessagingTemplateBackend',
)


# TODO Needs to be cached
def get_backend(backend=None):

    return load_class(backend or MESSAGING_BACKEND_CLASSES[0])