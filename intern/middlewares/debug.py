from pprint import pprint


class PostDebugMiddleware(object):

    def process_request(self, request):

        if request.POST:
            pprint(request.POST)