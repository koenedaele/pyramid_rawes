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
import warnings
import unittest

from .fixtures import (
    dummy_encoder,
    TestRegistry
)


class TestGetAndBuild(unittest.TestCase):

    def test_get_rawes(self):
        r = TestRegistry()
        ES = rawes.Elastic(url='http://localhost:9200')
        r.registerUtility(ES, IRawes, 'rawes')
        ES2 = get_rawes(r)
        self.assertEqual(ES, ES2)

    def test_build_rawes_already_exists(self):
        r = TestRegistry()
        ES = rawes.Elastic('http://localhost:9200')
        r.registerUtility(ES, IRawes, 'rawes')
        ES2 = _build_rawes(r)
        self.assertEqual(ES, ES2)

    def test_build_rawes_default_settings(self):
        r = TestRegistry()
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual(1, len(ES.connection_pool.connections))

    def test_build_rawes_custom_settings(self):
        settings = {
            'rawes.url': 'http://elastic.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123
        }
        r = TestRegistry(settings)
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual(1, len(ES.connection_pool.connections))

    def test_build_rawes_url_list_settings(self):
        settings = {
            'rawes.url': 'http://el1.search.org:9200\nhttp://el2.search.org:9200',
            'rawes.path': '/search',
            'rawes.timeout': 123
        }
        r = TestRegistry(settings)
        ES = _build_rawes(r)
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual(2, len(ES.connection_pool.connections))


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
        settings = {
                'rawes.url': 'http://elastic.search.org:9200\nhttp://elastic.search.org:9300',
        }
        args = _parse_settings(settings)
        self._assert_contains_all_keys(args)
        self.assertEqual(['http://elastic.search.org:9200', 'http://elastic.search.org:9300'], args['url'])

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
            'rawes.json_encoder': 'tests.fixtures.dummy_encoder'
        }
        args = _parse_settings(settings)
        self.assertEqual(dummy_encoder, args['json_encoder'])

    def test_list_settings(self):
        settings = {
            'rawes.url': 'http://el1.search.org:9200\nhttp://el2.search.org:9200'
        }
        args = _parse_settings(settings)
        self.assertEqual(
            [
                'http://el1.search.org:9200',
                'http://el2.search.org:9200'
            ], 
            args['url']
        )

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
        self.config.registry.settings['rawes.json_encoder'] = 'tests.fixtures.dummy_encoder'
        self.config.registry.settings['rawes.json_decoder'] = 'tests.fixtures.DummyDecoder'

    def tearDown(self):
        del self.config

    def test_includeme(self):
        includeme(self.config)
        ES = self.config.registry.queryUtility(IRawes, 'rawes')
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual(1, len(ES.connection_pool.connections))
        self.assertEqual('test', ES.json_encoder('test'))
        self.assertEqual(dummy_encoder, ES.json_encoder)
        self.assertEqual(
            {'test': 'DUMMY'},
            ES.connection_pool.connections[0].kwargs['json_decoder']('{"test": 1}')
        )

    def test_directive_was_added(self):
        includeme(self.config)
        ES = self.config.get_rawes()
        self.assertIsInstance(ES, rawes.Elastic)
        self.assertEqual(1, len(ES.connection_pool.connections))
