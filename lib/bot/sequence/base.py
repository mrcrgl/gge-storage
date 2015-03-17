from lib.bot.sequence.exceptions import TemporalExpressionError
from django.utils.timezone import now

import logging
logger = logging.getLogger(__name__)


class SequenceBrick(object):

    multiple_execution = False
    execution_count = 0
    sequence = None
    _action_fnc = None
    _expression_fnc = None

    def __init__(self):
        pass

    def is_available(self):
        if not self.multiple_execution and self.execution_count > 0:
            return False

        return True

    def check_expression(self, context, message):

        if hasattr(self._expression_fnc, '__call__'):
            result = self._expression_fnc.__call__(self, context, message)

            logger.info("Check expression [%s]: player=%s result=%s",
                        self.__class__.__name__, context.get_player(), result)

            return result

        logger.info("Check expression [%s]: player=%s result=%s function not provided",
                    self.__class__.__name__, context.get_player(), True)

        return True

    def perform_action(self, context, message):

        self.pre_action()

        if hasattr(self._action_fnc, '__call__'):
            logger.info("Perform action [%s]: function executed", self.__class__.__name__)
            context, message = self._action_fnc.__call__(self, context, message)
        else:
            logger.debug("Perform action [%s]: function not provided", self.__class__.__name__)

        self.post_action()
        return context, message

    def pre_action(self):
        pass

    def post_action(self):
        self.execution_count += 1

    def set_expression(self, fnc):
        self._expression_fnc = fnc

    def set_action(self, fnc):
        self._action_fnc = fnc


class Sequence():

    production_order = None
    bricks = None
    force_ordered = True
    closed = False
    max_expression_checks = 50
    current_expression_count = 0

    def __init__(self):
        pass

    def turn(self, context, message):
        bricks_available = 0

        for brick in self.bricks:
            if brick.is_available():
                bricks_available += 1
                try:
                    if brick.check_expression(context, message):
                        return brick.perform_action(context, message)
                    else:
                        self.current_expression_count += 1

                    if self.current_expression_count >= self.max_expression_checks:
                        raise TemporalExpressionError("Terminate Sequence: max expression count %d exceeded." %
                                                      self.max_expression_checks)
                except TemporalExpressionError, e:
                    reason = unicode(e).encode("utf-8")
                    logger.info("Brick forces to delay: player=%s delta=%s reason=%s",
                                context.get_player(), e.delta, reason)
                    self.faulty(reason=reason, delta=e.delta)
                    return context, message

                if self.force_ordered:
                    return context, message

        if not bool(bricks_available):
            self.finish()

        return context, message

    def append_brick(self, brick):
        if not self.bricks:
            self.bricks = []

        if isinstance(brick, SequenceBrick):
            self.bricks.append(brick)

    def release(self):
        self.close()

    def faulty(self, reason=None, delta=None):
        self.production_order.last_fault_reason = reason
        self.production_order.last_fault_date = now()
        self.production_order.save(update_fields=['last_fault_reason', 'last_fault_date'])
        self.finish(faulty=True, delta=delta)

    def finish(self, faulty=False, delta=None):
        self.close(faulty=faulty, delta=delta)

    def close(self, faulty=False, delta=None):
        logger.info("Sequence [%s]: closed faulty=%s", self.__class__.__name__, faulty)
        self.closed = True
        self.post_process(faulty=faulty, delta=delta)

    def is_closed(self):
        return self.closed

    def pre_process(self):
        pass

    def post_process(self, faulty=False, delta=None):
        pass
