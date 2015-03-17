from __future__ import unicode_literals

import json
from lib.proxy.timer import SetTimeout
from lib.proxy import commands

import logging
logger = logging.getLogger(__name__)


class ClientMixin(object):

    player_name = None

    def set_player_name(self, name):
        logger.info("Set player_name=%s", name if name else "None")
        self.player_name = name

    def server_to_client(self, msg):

        decoded = msg.decode('utf-8')

        # get new resource key
        if decoded.startswith("%xt%rsc%"):
            try:
                substr = decoded[decoded.index("%xt%rsc%"):]
                # logger.info("Substring: %s (%r)", substr, substr.split("%"))
                key = json.loads(substr.split("%")[5])['RS']
                self.set_resource_key(key)
            except KeyError:
                logger.exception("KeyError at: %s", "%xt%rsc%")

        if decoded.startswith("%xt%txi%") or decoded.startswith("%xt%txs%"):
            try:
                what = "%xt%txi%" if decoded.startswith("%xt%txi%") else "%xt%txs%"
                substr = decoded[decoded.index(what):]
                # logger.info("Substring: %s (%r)", substr, substr.split("%"))
                time_remaining = int(json.loads(substr.split("%")[5])['TX']['RT'])

                if time_remaining < 0:
                    time_remaining = 0

                time_remaining += 5
                logger.info("TAX: set timeout to %d", time_remaining)
                self.set_timeout('tax_collect', SetTimeout(commands.collect_tax, time_remaining))
            except KeyError:
                logger.exception("KeyError at: %s", "%xt%txi%")

        if decoded.startswith("%xt%irc%"):
            self.set_timeout('irc_collect', SetTimeout(commands.collect_walking_resources, 5))
            return None

        if decoded.startswith("%xt%rcc%"):  # or decoded.startswith("%xt%jaa%"):
            logger.debug("RCC data found: %s", decoded)
            try:
                what = "%xt%rcc%" if decoded.startswith("%xt%rcc%") else "%xt%jaa%"
                substr = decoded[decoded.index(what):]
                logger.debug("RCC substr: %s", substr)
                data = json.loads(substr.split("%")[5])
                logger.debug("RCC data: %r", data)

                rci = data.get("rci", {})

                rt0 = rci.get("RC")[0].get("RS")
                rt1 = rci.get("RC")[1].get("RS")
                rt2 = rci.get("RC")[2].get("RS")

                duration = rt1 if rt0 > rt1 else rt0
                duration = rt2 if duration > rt2 else duration

                if duration == rt0:
                    rt = 0
                elif duration == rt1:
                    rt = 1
                elif duration == rt2:
                    rt = 2
                else:
                    return

                if duration <= 1:
                    duration = 1

                duration += 5

                logger.info("BOT: RCC-%d detected. Set timeout=%d", rt, duration)

                self.set_timeout(
                    'rcc_collect',
                    SetTimeout(
                        commands.handmade_command(
                            'rcc',
                            {
                                'RT': rt
                            }
                        ),
                        duration
                    )
                )
            except KeyError:
                logger.exception("KeyError at: %s", "%xt%rcc%")
            except ValueError:
                logger.exception("ValueError at: %s", "%xt%rcc%")

        if False and decoded.startswith("%xt%gbd%"):
            try:
                substr = decoded[decoded.index("%xt%gbd%"):]
                data = json.loads(substr.split("%")[5])
                logger.info("GBD: %r", data)
                self.set_player_name(data.get("gpi", {}).get("PN", None))
            except KeyError:
                logger.exception("KeyError at: %s", "%xt%gbd%")
            except ValueError:
                logger.exception("ValueError at: %s", "%xt%gbd%")


        return msg