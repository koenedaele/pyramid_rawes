# -*- coding: utf8 -*-

from pyramid_rawes import (
    IRawES,
    get_rawes,
    _build_rawes
    )

import rawes

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestRegistry(object):

    def __init__(self, settings=None):

        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        self.rawes = None

    def queryUtility(self, iface):
        return self.rawes

    def registerUtility(self, rawes, iface):
        self.rawes = rawes

class TestGetAndBuild(unittest.TestCase):

    def test_get_rawes(self):
        r = TestRegistry()
        ES = rawes.Elastic('')
        r.registerUtility(ES, IRawES)
        ES2 = get_rawes(r)
        self.assertEquals(ES, ES2)

    def test_build_rawes_already_exists(self):
        r = TestRegistry()
        ES = rawes.Elastic('')
        r.registerUtility(ES, IRawES)
        ES2 = _build_rawes(r)
        self.assertEquals(ES, ES2)

    def test_build_rawes_minimal_settings(self):
        r = TestRegistry({
            'es.uri': ''
            })
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
