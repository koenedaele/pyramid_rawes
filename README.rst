pyramid_rawes
=============

This library helps integrate rawes_ in a pyramid application.

.. image:: https://travis-ci.org/koenedaele/pyramid_rawes.png
        :target: https://travis-ci.org/koenedaele/pyramid_rawes

Installation
------------

To install pyramid_rawes, use pip

.. code-block:: bash
    
    pip install pyramid_rawes

Setup
-----

To activate pyramid_rawes

.. code-block:: python

    config = Configurator()
    config.include('pyramid_rawes')


By default, this will add an instance with all the default parameters 
(eg. Elastic Search is assumed to run at localhost:9200). To configure your 
rawes_ instance, you can use the pyramid settings file.

.. code-block:: ini

    rawes.url = localhost:9500
    rawes.connection_type = http

Once you have activated pyramid_rawes, a rawes_ instance is added to the registry.

Usage
-----

To get a rawes_ instance, call get_rawes with the current application registry. 
Eg. in a view:

.. code-block:: python

    from pyramid_rawes import get_rawes

    def search(request):
        ES = get_rawes(request.registry)
        # execute search
        # ...

.. _rawes: https://github.com/humangeo/rawes
