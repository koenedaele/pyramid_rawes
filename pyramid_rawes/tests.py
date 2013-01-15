# -*- coding: utf8 -*-

from pyramid import testing

from pyramid_rawes import (
    IRawES,
    get_rawes,
    _build_rawes,
    includeme,
    _parse_settings
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

    def test_build_rawes_default_settings(self):
        r = TestRegistry()
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)

    def test_build_rawes_custom_settings(self):
        settings = {
            'rawes.url': 'elastic.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123,
            'rawes.connection_type': 'http',
            'rawes.except_on_error': True
            }
        r = TestRegistry(settings)
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEquals('elastic.search.org:9200', ES.url)


class TestSettings(unittest.TestCase):

    def _assert_contains_all_keys(self, args):
        self.assertIn('url', args)
        self.assertIn('path', args)
        self.assertIn('connection_type', args)
        self.assertIn('except_on_error', args)
        self.assertIn('timeout', args)

    def test_get_default_settings(self):
        settings = {}
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)

    def test_get_some_settings(self):
        settings = {
            'rawes.url': 'elastic.search.org:9200',
            'rawes.timeout': 123,
            'rawes.except_on_error': True
            }
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)
        self.assertEquals('elastic.search.org:9200', args['url'])
        self.assertEquals(123, args['timeout'])
        self.assertEquals(True, args['except_on_error'])

    def test_get_all_settings(self):
        settings = {
            'rawes.url': 'elastic.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123,
            'rawes.connection_type': 'http',
            'rawes.except_on_error': True
            }
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)
        self.assertEquals(123, args['timeout'])
        self.assertEquals(True, args['except_on_error'])

class TestIncludeMe(unittest.TestCase):

    def test_includeme(self):
        config = testing.setUp()
        config.registry.settings['rawes.url'] = 'localhost:9300'
        includeme(config)
        ES = config.registry.queryUtility(IRawES)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEquals('localhost:9300', ES.url)
        
