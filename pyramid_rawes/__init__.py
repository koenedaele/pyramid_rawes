# -*- coding: utf8 -*-

import rawes

from pyramid.settings import aslist

from zope.interface import Interface

from rawes.encoders import encode_date_optional_time

from pyramid.path import (
    DottedNameResolver
)

import warnings


class IRawes(Interface):
    pass


def _parse_settings(settings):

    rawes_args = {}
    defaults = {
        'url': 'http://localhost:9200',
        'timeout': 30,
        'path': '',
        'json_encoder': encode_date_optional_time,
    }

    rawes_args = defaults.copy()

    # set string settings
    for short_key_name in ('path',):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                settings.get(key_name, defaults.get(short_key_name))

    # set list settings
    for short_key_name in ('url',):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                (aslist(settings.get(key_name, defaults.get(short_key_name)))
		        if len(aslist(settings.get(key_name, defaults.get(short_key_name)))) > 1
		        else settings.get(key_name, defaults.get(short_key_name)).strip())

    # integer settings
    for short_key_name in ('timeout',):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            rawes_args[short_key_name] = \
                int(settings.get(key_name, defaults.get(short_key_name)))

    # function settings
    for short_key_name in ('json_encoder',):
        key_name = 'rawes.%s' % (short_key_name,)
        r = DottedNameResolver()
        if key_name in settings:
            rawes_args[short_key_name] = \
                r.resolve(settings.get(key_name))
    for short_key_name in ('json_decoder',):
        key_name = 'rawes.%s' % (short_key_name,)
        r = DottedNameResolver()
        if key_name in settings:
            rawes_args[short_key_name] = \
                r.resolve(settings.get(key_name))().decode

    # removed settings
    for short_key_name in ('connection_type', 'except_on_error'):
        key_name = 'rawes.%s' % (short_key_name,)
        if key_name in settings:
            warnings.warn(
                '%s is no longer supported, please remove from your settings.',
                UserWarning
            )

    return rawes_args


def _build_rawes(registry):
    """
    Build a RawES connection to Elastic Search and add it to the registry.
    """
    ES = registry.queryUtility(IRawes, 'rawes')
    if ES is not None:
        return ES

    settings = registry.settings
    rawes_args = _parse_settings(settings)

    ES = rawes.Elastic(**rawes_args)

    registry.registerUtility(ES, IRawes, 'rawes')
    return registry.queryUtility(IRawes, 'rawes')


def get_rawes(registry):
    """
    Get the RawES connection.
    """
    #Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IRawes, 'rawes')


def includeme(config):
    _build_rawes(config.registry)
    config.add_directive('get_rawes', get_rawes)
