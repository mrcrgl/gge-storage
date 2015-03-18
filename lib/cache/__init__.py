from threading import local

from django.conf import settings
from django.core import signals
from django.core.cache.backends.base import (
    InvalidCacheBackendError, CacheKeyWarning, BaseCache)
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
import os


__all__ = [
    'cache', 'DEFAULT_CACHE_ALIAS', 'InvalidCacheBackendError',
    'CacheKeyWarning', 'BaseCache',
]

DEFAULT_CACHE_ALIAS = 'default'

if DEFAULT_CACHE_ALIAS not in settings.CACHES:
    raise ImproperlyConfigured("You must define a '%s' cache" % DEFAULT_CACHE_ALIAS)


def _create_cache(backend, **kwargs):
    try:
        # Try to get the CACHES entry for the given backend name first
        try:
            conf = settings.CACHES[backend]
        except KeyError:
            try:
                # Trying to import the given backend, in case it's a dotted path
                import_string(backend)
            except ImportError as e:
                raise InvalidCacheBackendError("Could not find backend '%s': %s" % (
                    backend, e))
            location = kwargs.pop('LOCATION', '')
            params = kwargs
        else:
            params = conf.copy()
            params.update(kwargs)
            backend = params.pop('BACKEND')
            location = params.pop('LOCATION', '')
        backend_cls = import_string(backend)
    except ImportError as e:
        raise InvalidCacheBackendError(
            "Could not find backend '%s': %s" % (backend, e))
    return backend_cls(location, params)


class CacheHandler(object):
    """
    A Cache Handler to manage access to Cache instances.
    Ensures only one instance of each alias exists per thread.
    """
    def __init__(self):
        self._caches = local()

    def __getitem__(self, alias_pid):
        try:
            return self._caches.caches[alias_pid]
        except AttributeError:
            self._caches.caches = {}
        except KeyError:
            pass

        alias, pid = alias_pid.split('-')

        if alias not in settings.CACHES:
            raise InvalidCacheBackendError(
                "Could not find config for '%s' in settings.CACHES" % alias
            )

        cache = _create_cache(alias)
        self._caches.caches[alias_pid] = cache
        return cache

    def all(self):
        return getattr(self._caches, 'caches', {}).values()

caches = CacheHandler()


class DefaultCacheProxy(object):
    """
    Proxy access to the default Cache object's attributes.
    This allows the legacy `cache` object to be thread-safe using the new
    ``caches`` API.
    """
    def __getattr__(self, name):
        return getattr(caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))], name)

    def __setattr__(self, name, value):
        return setattr(caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))], name, value)

    def __delattr__(self, name):
        return delattr(caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))], name)

    def __contains__(self, key):
        return key in caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))]

    def __eq__(self, other):
        return caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))] == other

    def __ne__(self, other):
        return caches['-'.join((DEFAULT_CACHE_ALIAS, str(os.getpid())))] != other

cache = DefaultCacheProxy()


def close_caches(**kwargs):
    # Some caches -- python-memcached in particular -- need to do a cleanup at the
    # end of a request cycle. If not implemented in a particular backend
    # cache.close is a no-op
    for cache in caches.all():
        cache.close()
signals.request_finished.connect(close_caches)