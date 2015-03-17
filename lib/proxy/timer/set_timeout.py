__author__ = 'marc'


class SetTimeout():

    ticks = None
    function = None

    def __init__(self, fnc, timeout):
        self.ticks = timeout
        self.function = fnc

    def exceed(self):
        return self.ticks <= 0

    def tick(self, proxy):
        self.ticks -= proxy.throttle

        if not self.exceed():
            return False

        self.function(proxy)
        return True