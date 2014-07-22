# -*- coding: utf8 -*-

import json


def dummy_encoder(obj):
    return obj


class DummyDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        for k, v in d.items():
            d[k] = 'DUMMY'
        return d


class TestRegistry(object):

    def __init__(self, settings=None):

        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        self.rawes = None

    def queryUtility(self, iface, name):
        return self.rawes

    def registerUtility(self, rawes, iface, name):
        self.rawes = rawes
