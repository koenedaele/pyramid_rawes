# -*- coding: utf8 -*-

import rawes
from rawes.elastic_exception import ElasticException

from zope.interface import Interface

class IRawES(Interface):
    pass

def _build_rawes(registry):
    """
    Build a RawES connection to Elastic Search and add it to the registry.
    """
    ES = registry.queryUtility(IRawES)
    if ES is not None:
        return ES

    settings = registry.settings

    ES = rawes.Elastic(settings['es.uri'])

    registry.registerUtility(ES, IRawES)
    return registry.queryUtility(IRawES)

def get_rawes(registry):
    """
    Get the RawES connection.
    """
    return registry.queryUtility(IRawES)

def includeme(config):
    _build_rawes(config.registry)
