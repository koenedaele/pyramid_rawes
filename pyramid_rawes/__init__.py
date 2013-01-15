# -*- coding: utf8 -*-

import rawes
from rawes.elastic_exception import ElasticException

from pyramid.settings import asbool

from zope.interface import Interface

class IRawES(Interface):
    pass

def _parse_settings(settings):

    rawes_args = {}
    defaults = {
        'url': 'localhost:9200',
        'timeout': 30,
        'except_on_error': False,
        'path': '',
        'connection_type': None
    }

    rawes_args = defaults.copy()

    # set string settings
    for short_key_name in ('url', 'path', 'connection_type'):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                settings.get(key_name, defaults.get(short_key_name))

    # boolean settings
    for short_key_name in ('except_on_error',):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                asbool(settings.get(key_name, defaults.get(short_key_name)))

    # integer settings
    for short_key_name in ('timeout',):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                int(settings.get(key_name, defaults.get(short_key_name)))

    return rawes_args

def _build_rawes(registry):
    """
    Build a RawES connection to Elastic Search and add it to the registry.
    """
    ES = registry.queryUtility(IRawES)
    if ES is not None:
        return ES

    settings = registry.settings
    rawes_args = _parse_settings(settings)

    ES = rawes.Elastic(rawes_args['url'], 
                       rawes_args['path'], 
                       rawes_args['timeout'],
                       rawes_args['connection_type'],
                       None,
                       rawes_args['except_on_error']
                       )

    registry.registerUtility(ES, IRawES)
    return registry.queryUtility(IRawES)

def get_rawes(registry):
    """
    Get the RawES connection.
    """
    return registry.queryUtility(IRawES)

def includeme(config):
    _build_rawes(config.registry)
