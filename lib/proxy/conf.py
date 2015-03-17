from __future__ import unicode_literals

import os

EMPIRE = 'EmpireEx_2'
EMPIRE4K = 'EmpirefourkingdomsExGG'

GAMES = [EMPIRE, EMPIRE4K]

settings = {
    "STORAGE_HOST": ('0.0.0.0', 7766),
    "STORAGE": 's',
    "ENDPOINT": 'e',
    "CLIENT": 'c'
}

settings['DISABLE_PARTIALS_FOR'] = (
    settings.get("CLIENT"),
    settings.get("ENDPOINT"),
    settings.get("STORAGE")
)

game_specific = {
    EMPIRE: {
        'PROXY_BIND': ('0.0.0.0', 8028),
        'ENDPOINT_HOST': ('78.138.113.215', 8029),
        'GAME': EMPIRE,
        'PRODUCT_NUMBER': 2
    },
    EMPIRE4K: {
        'PROXY_BIND': ('0.0.0.0', 8018),
        'ENDPOINT_HOST': ('78.138.113.215', 8019),
        'GAME': EMPIRE4K,
        'PRODUCT_NUMBER': 1
    }
}

game = os.environ.get("GAME", None)

if not game or not game in GAMES:
    raise EnvironmentError("Missing ENV GAME. Should be one of (%r)" % GAMES)

settings.update(game_specific.get(game, {}))


def get_settings(game):
    settings.update(game_specific.get(game, {}))
    return settings