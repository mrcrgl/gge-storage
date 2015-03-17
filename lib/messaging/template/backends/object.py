
class TemplateDoesNotExist(Exception):
    pass


class DefaultMessagingTemplateBackend(object):

    def get_template(self, slug):
        raise NotImplementedError()