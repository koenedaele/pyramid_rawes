# -*- coding: utf8 -*-

from pyramid import testing

from pyramid_rawes import (
    IRawes,
    get_rawes,
    _build_rawes,
    includeme,
    _parse_settings
)

import rawes
import json
import warnings

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

def dummy_encoder(obj):
    return obj

class DummyDecoder(json.JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
    
    def dict_to_object(self, d):
        for k,v in d.items():
            d[k] = 'DUMMY'
        return d

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
        ES = rawes.Elastic(url='http://localhost:9200')
        r.registerUtility(ES, IRawes)
        ES2 = get_rawes(r)
        self.assertEqual(ES, ES2)

    def test_build_rawes_already_exists(self):
        r = TestRegistry()
        ES = rawes.Elastic('http://localhost:9200')
        r.registerUtility(ES, IRawes)
        ES2 = _build_rawes(r)
        self.assertEqual(ES, ES2)

    def test_build_rawes_default_settings(self):
        r = TestRegistry()
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual('localhost:9200', ES.url.netloc)

    def test_build_rawes_custom_settings(self):
        settings = {
            'rawes.url': 'http://elastic.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123
        }
        r = TestRegistry(settings)
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual('elastic.search.org:9200', ES.url.netloc)


class TestSettings(unittest.TestCase):

    def _assert_contains_all_keys(self, args):
        self.assertIn('url', args)
        self.assertIn('path', args)
        self.assertIn('timeout', args)

    def test_get_default_settings(self):
        settings = {}
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)

    def test_get_some_settings(self):
        settings = {
            'rawes.url': 'http://elastic.search.org:9200',
            'rawes.timeout': 123,
        }
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)
        self.assertEqual('http://elastic.search.org:9200', args['url'])
        self.assertEqual(123, args['timeout'])

    def test_get_all_settings(self):
        settings = {
            'rawes.url': 'http://elastic.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123,
        }
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)
        self.assertEqual(123, args['timeout'])

    def test_get_dotted_function_settings(self):
        settings = {
            'rawes.json_encoder': 'pyramid_rawes.tests.dummy_encoder'
        }
        args = _parse_settings(settings)
        self.assertEqual(dummy_encoder, args['json_encoder'])

    def test_get_unsupported_settings(self):
        settings = {
            'rawes.except_on_error': False
        }
        with warnings.catch_warnings(record=True) as w:
            args = _parse_settings(settings)
            self.assertEqual(1, len(w))

class TestIncludeMe(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.registry.settings['rawes.url'] = 'http://localhost:9300'
        self.config.registry.settings['rawes.json_encoder'] = 'pyramid_rawes.tests.dummy_encoder'
        self.config.registry.settings['rawes.json_decoder'] = 'pyramid_rawes.tests.DummyDecoder'

    def tearDown(self):
        del self.config

    def test_includeme(self):
        includeme(self.config)
        ES = self.config.registry.queryUtility(IRawes)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual('localhost:9300', ES.url.netloc)
        self.assertEqual('test',ES.json_encoder('test'))
        self.assertEqual(dummy_encoder, ES.json_encoder)
        self.assertEqual({'test': 'DUMMY'}, ES.connection.kwargs['json_decoder']('{"test": 1}'))

    def test_directive_was_added(self):
        includeme(self.config)
        ES = self.config.get_rawes()
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual('localhost:9300', ES.url.netloc)
