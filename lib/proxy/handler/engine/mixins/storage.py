from __future__ import unicode_literals

import json

import logging
logger = logging.getLogger(__name__)


class StorageMixin(object):

    #resource_key = 1
    #product_name = "EmpireEx_2"
    #product_number = 2
    #close_bit = "\x00"

    def execute_storage_command(self, message):
        decoded = message.decode('utf-8')

        logger.info("execute_storage_command: %r", decoded)

        if decoded.startswith("%px%GGEStorage%fwd_srv%"):
            logger.info("decoded.startswith: %r", decoded)

            #try:
            substr = decoded[decoded.index("%px%GGEStorage%fwd_srv%"):]
            request = json.loads(substr.split("%")[5])
            command = request['cmd']
            data = request['data']
            data_string = json.dumps(data, separators=(',', ':'))

            if "##RSKEY##" in data_string:
                if not self.resource_key:
                    return

                data_string = data_string.replace('"##RSKEY##"', unicode(self.resource_key))

            response = "%".join((
                "",
                "xt",
                self.product_name,
                command,
                unicode(self.product_number),
                data_string,
                self.close_bit
            ))

            logger.info("FWD_SRV: %s", response)

            self.to_server(response)
            #except KeyError:
            #    logger.exception("FWD_SRV failed with KeyError: %r", decoded)
            #finally:
            #    logger.info("decoded.startswith :: finally: %r", decoded)
            #    return