import os
from .basics import *


DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'gunicorn',
)

# remove: django.middleware.common.CommonMiddleware
OLD_MIDDLEWARE_CLASSES = tuple()
for middleware in MIDDLEWARE_CLASSES:
    if middleware != "django.middleware.common.CommonMiddleware":
        OLD_MIDDLEWARE_CLASSES += (middleware,)

MIDDLEWARE_CLASSES = (
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
) + OLD_MIDDLEWARE_CLASSES

CACHE_MIDDLEWARE_SECONDS = 120
CACHE_MIDDLEWARE_KEY_PREFIX = 'www'

EXCLUDE_FROM_MINIFYING = ('^management/', '^admin/',)

ALLOWED_HOSTS = '*'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file_access': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/django.log',
            'formatter': 'verbose'
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/django.log',
            'formatter': 'verbose'
        },
        'file_socket': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/socket.log',
            'formatter': 'verbose'
        },
        'file_proxy': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/proxy.log',
            'formatter': 'verbose'
        },
        'file_pushover': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/pushover.log',
            'formatter': 'verbose'
        },
        'file_explorer': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/explorer.log',
            'formatter': 'verbose'
        },
        'file_exceptions': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/exception.log',
            'formatter': 'verbose'
        },
        'file_messages': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/messages.log',
            'formatter': 'verbose'
        },
        'file_models': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/gge/model.log',
            'formatter': 'verbose'
        },
        'file_context': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/context.log',
            'formatter': 'verbose'
        },
        'file_middleware': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/middleware.log',
            'formatter': 'verbose'
        },
        'file_sequence': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'filename': '/var/log/gge/sequence.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'mail_admins', 'file_exceptions'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'file_exceptions'],
            'level': 'ERROR',
            'propagate': True,
        },
        'gge_proxy_manager': {
            'handlers': ['file_models', 'file_exceptions'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.socket': {
            'handlers': ['file_socket', 'file_exceptions'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.socket.context': {
            'handlers': ['file_context'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.socket.middleware': {
            'handlers': ['file_middleware'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.socket.middleware.log': {
            'handlers': ['file_messages'],
            'propagate': False,
            'level': 'DEBUG',
            #'filters': ['special']
        },
        'lib.socket.middleware.map_explorer': {
            'handlers': ['file_explorer'],
            'propagate': False,
            'level': 'INFO',
            #'filters': ['special']
        },
        'lib': {
            'handlers': ['mail_admins', 'file_exceptions'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lib.core': {
            'handlers': ['file_socket'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.bot.sequence': {
            'handlers': ['file_sequence'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            #'filters': ['special']
        },
        'lib.proxy': {
            'handlers': ['file_proxy'],
            'level': 'DEBUG',
            'propagate': True,
            #'filters': ['special']
        },
        'pushover': {
            'handlers': ['file_pushover'],
            'level': 'INFO',
            'propagate': False,
            #'filters': ['special']
        },
    }
}

if not DEBUG:
    STATIC_URL = 'http://static.gge.bam.st/'

if not DEBUG:
    try:
        from git import Repo
        repo = Repo(ROOT_DIR)

        for head in repo.heads:
            if not head.name == 'master':
                continue

            DEPLOYMENT_ID = unicode(head.commit)[:6]
    except:
        DEPLOYMENT_ID = ''
