"""
Django settings for gge_storage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

from ConfigParser import RawConfigParser

config = RawConfigParser()

config_file = os.path.expanduser('~/.gge_storage/settings.ini')
if os.path.exists(config_file):
    config.read(os.path.expanduser(config_file))
else:
    config.read(os.path.join((ROOT_DIR, 'settings-example.ini'))
        
ADMINS = tuple(config.items('error mail'))
MANAGERS = tuple(config.items('404 mail'))

DEBUG = config.getboolean('debug', 'DEBUG')
SECRET_KEY = config.get('secrets', 'SECRET_KEY')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #'djangocms_file',
    #'djangocms_flash',
    #'djangocms_googlemap',
    #'djangocms_inherit',
    #'djangocms_picture',
    #'djangocms_teaser',
    #'djangocms_video',
    # 'djangocms_link',
    #'djangocms_snippet',

    #'djangocms_grid',
    #'djangocms_column',
    'djangocms_text_ckeditor',

    'cms',
    'menus',
    'reversion',
    'djangocms_admin_style',
    'mptt',
    'easy_thumbnails',
    'filer',
    'djcelery',
    'lib.socket',
    'lib.proxy',
    'lib.messaging',
    'pushover',
    'gge_proxy_manager',
    'frontend',
    'authentication',
    'intern',
    'npc',
    'templated_forms',
    'sekizai',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',

    'intern.middlewares.player.EnrichPlayerMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
)

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

MIGRATION_MODULES = {
    'filer': 'filer.migrations_django',
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
    'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
    'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',

    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',

    # Add also the following modules if you're using these plugins:
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_video': 'djangocms_video.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
}

ROOT_URLCONF = 'gge_storage.urls'

WSGI_APPLICATION = 'gge_storage.wsgi.application'


CMS_TEMPLATES = (
    ('_base.html', 'Base Layout'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGES = (
    ('de', 'German'),
)
LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

INTERNAL_IPS = tuple(config.get('debug', 'INTERNAL_IPS').split())

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
STATIC_URL = config.get('common', 'STATIC_URL')

#STATICFILES_DIRS = (
#    os.path.join(ROOT_DIR, "static_basic"),
#)

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../media'))
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "../templates"),
)

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/intern'

SOCKET_MIDDLEWARE_CLASSES = (
    'lib.socket.middleware.auth.AuthMiddleware',
    'lib.socket.middleware.game_recognition.GameRecognitionMiddleware',
    'lib.socket.middleware.global_data.GlobalDataMiddleware',
    'lib.socket.middleware.collector.CollectorMiddleware',
    'lib.socket.middleware.goods_count.GoodsCollectedMiddleware',
    'lib.socket.middleware.resource_count.ResourceCountMiddleware',
    'lib.socket.middleware.logistic_job.LogisticJobMiddleware',
    'lib.socket.middleware.ping.PingMiddleware',
    'lib.socket.middleware.resource_key.ResourceKeyMiddleware',
    'lib.socket.middleware.production.ProductionMiddleware',
    'lib.socket.middleware.geotracking.GeotrackingMiddleware',
    'lib.socket.middleware.afk.AfkMiddleware',
    'lib.socket.middleware.alliance.AllianceMiddleware',
    'lib.socket.middleware.attack.AttackLogMiddleware',
    'lib.socket.middleware.map_explorer.MapExplorerMiddleware',
    'lib.socket.middleware.castle_economy.CastleEconomyMiddleware',
    'lib.socket.middleware.log.LogMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        #'django': {
        #    'handlers': ['null'],
        #    'propagate': True,
        #    'level': 'INFO',
        #},
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'gge_proxy_manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
            #'filters': ['special']
        },
        'lib': {
            'handlers': ['console'],
            'level': 'DEBUG',
            #'filters': ['special']
        }
    }
}

# DEFAULT_FROM_EMAIL = 'root@bam.st'
# SERVER_EMAIL = DEFAULT_FROM_EMAIL
# EMAIL_HOST = 'post.bam.st'
# EMAIL_HOST_PASSWORD = 'Buwuta81Godafo66'
# EMAIL_HOST_USER = 'gge@bam.st'
# EMAIL_SUBJECT_PREFIX = '[GGE] '
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = config.get('email', 'FROM_EMAIL')
SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_PASSWORD')
EMAIL_HOST_USER = config.get('email', 'EMAIL_USER')
EMAIL_SUBJECT_PREFIX = config.get('email', 'SUBJECT_PREFIX')
EMAIL_USE_TLS = config.getboolean('email', 'USE_TLS')
EMAIL_USE_SSL = config.getboolean('email', 'USE_SSL')

# Celery
import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = BROKER_URL  # 'database'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

NOTIFY_NEW_RUIN = {
    "EmpireEx_2": (
    ),
    "EmpirefourkingdomsExGG": (
    ),
}

PUSHOVER_APP_TOKEN = config.get('pushover', 'APP_TOKEN')
PUSHOVER_NEW_RUIN_TOKEN = config.get('pushover', 'NEW_RUIN_TOKEN')

LOGIN_SERVICE_URL = config.get('login service', 'URL')
LOGIN_SERVICE_SECRET = config.get('login service', 'SECRET')

DEPLOYMENT_ID = '@dev'
