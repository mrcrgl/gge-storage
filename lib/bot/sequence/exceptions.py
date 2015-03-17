from django.utils.timezone import timedelta


class TemporalExpressionError(Exception):
    delta = timedelta(minutes=25)

    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args)
        delta = kwargs.get('delta', None)
        if delta:
            self.delta = delta


class ShortTemporalExpressionError(TemporalExpressionError):
    delta = timedelta(minutes=5)


class LongTemporalExpressionError(TemporalExpressionError):
    delta = timedelta(minutes=60)