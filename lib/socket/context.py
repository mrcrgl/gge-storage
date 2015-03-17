from __future__ import unicode_literals

from gge_proxy_manager.models import Kingdom
from django.utils.timezone import now, timedelta
from .exceptions import DeadConnectionException

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class RequestContext(object):

    def __init__(self, socket):
        self.socket = socket
        self.responses = []
        self.session = {}
        self.production_slots = {}
        self.silence_counter = 0

    locked_until = None
    locked_for = None
    locked_by = None
    locked_infinite_by = None

    def lock_for(self, seconds, by=None, module='global'):
        self.locked_until = now() + timedelta(seconds=seconds)
        self.locked_for = module
        self.locked_by = by
        logger.info("Context is locked by=%s for=%s until=%s" % (self.locked_by, self.locked_for, self.locked_until))

    def is_locked(self, module=None):
        return True if self.locked_infinite_by or (self.locked_until and now() < self.locked_until) else False

    def is_locked_for(self, module=None):
        pass

    def lock_infinite_for(self, name):
        self.locked_infinite_by = name

    def unlock(self, name=None):
        self.locked_until = None

        if name and self.locked_infinite_by and self.locked_infinite_by == name:
            self.locked_infinite_by = None

        logger.info("Context is unlocked")

    session = None

    def session_get(self, key):
        try:
            return self.session.get(key, None)
        except KeyError:
            return None

    def session_set(self, key, value):
        self.session[key] = value

    def session_unset(self, key):
        try:
            del self.session[key]
        except KeyError:
            pass

    production_slots = None

    def set_production_slots(self, castle, nbr, slots):
        key = "-".join((unicode(castle.pk), unicode(nbr)))

        self.production_slots[key] = []

        for slot in slots:
            if slot[0] == -2:
                continue

            else:
                self.production_slots[key].append(now() + timedelta(seconds=slot[0]))

    def are_slots_locked_2(self, castle, nbr):
        return bool(self.get_free_slot_count(castle, nbr) == 0)

    def next_slot_available_in(self, castle, nbr):
        key = "-".join((unicode(castle.pk), unicode(nbr)))

        if not key in self.production_slots or not len(self.production_slots[key]):
            return None

        smallest_delta = None
        for slot in self.production_slots[key]:
            if now() > slot:
                delta = slot - now()

                if delta < smallest_delta or smallest_delta is None:
                    smallest_delta = delta

        return smallest_delta

    def are_slots_locked(self, castle, nbr):
        key = "-".join((unicode(castle.pk), unicode(nbr)))

        if not key in self.production_slots:
            self.production_slots[key] = []

        if not len(self.production_slots[key]):
            return False

        for slot in self.production_slots[key]:
            if now() > slot:
                return False

        return True

    def get_free_slot_count(self, castle, nbr):
        key = "-".join((unicode(castle.pk), unicode(nbr)))
        available = 0

        if not key in self.production_slots:
            return available

        if not len(self.production_slots[key]):
            return available

        for slot in self.production_slots[key]:
            if slot < now():
                available += 1

        return available

    # deprecated?
    conn = None
    responses = None
    username = None
    player = None
    is_afk = None
    kingdom = None
    castle = None
    game = None
    available_kingdoms = None
    has_dealer_until = None

    def add_response(self, message):
        self.responses.append(message)

    def pop_response(self):
        return self.responses.pop()

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return bool(self.username)

    def set_kingdom(self, kingdom):
        logger.info("Set kingdom to: %s" % kingdom.name)
        self.kingdom = kingdom

    def get_kingdom(self):
        return self.kingdom

    def set_game(self, game):
        logger.info("Set game to: %s" % game.name)
        self.game = game

    def get_game(self):
        return self.game

    def set_castle(self, castle):
        logger.info("Set castle to: %s" % castle.name)
        self.castle = castle
        self.set_player(castle.player)
        self.set_kingdom(castle.kingdom)

    def get_castle(self):
        return self.castle

    def set_player(self, player):
        logger.info("Set player to: %s" % player.name)
        self.player = player

    def get_player(self):
        return self.player

    def set_afk(self, afk):
        logger.info("Set AFK: %s" % bool(afk))
        self.is_afk = bool(afk)

        # Lock for a minute to avoid changing kingdom while playing
        if self.is_afk:
            self.lock_for(60)

    def add_dealer(self, seconds):
        self.has_dealer_until = now() + timedelta(seconds=seconds)
        logger.info("Dealer added. Valid until (%ds) %s", seconds, self.has_dealer_until)

    def has_dealer(self):
        return self.has_dealer_until and self.has_dealer_until > now()

    def get_available_kingdoms(self):
        if not self.available_kingdoms:
            if not self.get_player():
                return []

            try:
                self.available_kingdoms = Kingdom.objects.filter(castle__player=self.get_player()).distinct()
                logger.info(
                    "Set available kingdoms to: %s", ", ".join([kingdom.name for kingdom in self.available_kingdoms])
                )
            except TypeError as e:
                logger.exception("Error while fetching available kingdoms for user=%s", self.get_player())

        return self.available_kingdoms

    silence_counter = None

    def is_silent(self):
        self.silence_counter += 1

        if self.silence_counter >= 25:
            raise DeadConnectionException()

    def is_not_silent(self):
        self.silence_counter = 0