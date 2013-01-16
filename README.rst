pyramid_rawes
=============

This library helps integrate RawES_ in a pyramid application.

.. image:: https://travis-ci.org/koenedaele/pyramid_rawes.png
        :target: https://travis-ci.org/koenedaele/pyramid_rawes

Installation
------------

To install pyramid_rawes, use pip

.. code-block:: bash
    
    pip install pyramid_rawes

Setup
-----

To activate pyramid_rawes::

    config = Configurator()
    config.include('pyramid_rawes')

Once you have activated pyramid_rawes, a RawES_ instance is added to the registry.

Usage
-----

To get a RawES_ instance, call get_rawes with the current application registry. 
Eg. in a view::

    from pyramid_rawes import get_rawes

    def search(request):
        ES = get_rawes(request.registry)
        # execute search
        # ...

.. _RawES: https://github.com/humangeo/rawes
