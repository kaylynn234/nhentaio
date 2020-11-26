.. toctree::
   :maxdepth: 3


API reference
==============

Client
-------
.. automodule:: nhentaio.client
   :members:

Query
------
.. automodule:: nhentaio.query
   :members:

Enums
------

SortType
~~~~~~~~~
.. automodule:: nhentaio.enums
   :members:
   :undoc-members:

Models
-------

Gallery
~~~~~~~~
.. autoclass:: nhentaio.Gallery

PartialGallery
~~~~~~~~~~~~~~~
.. autoclass:: nhentaio.PartialGallery

GalleryPage
~~~~~~~~~~~~
.. autoclass:: nhentaio.GalleryPage

Taglike
~~~~~~~~
.. automodule:: nhentaio.taglike
   :members:


Asset
~~~~~~
.. automodule:: nhentaio.asset
   :members:

Asynchronous iterators
-----------------------
Various parts of this library return what is referred to as an asynchronous iterator (or ``AsyncIterator`` in shortened form)
These can be used in an ``async for`` statement:

.. code-block:: python

    async for gallery in client.search("full color"):
        # do something with gallery here

There are of course other things you can do with asynchronous iterators as well:

.. class:: AsyncIterator

    Represents the concept of an asynchronous iterator. Note that there is no "AsyncIterator" class - it is purely abstract.
    
    .. method:: next()
        :async:

        Advances the iterator by one if possible. If there are no more items, this raises :exc:`NoMoreItems`.

    .. method:: flatten()
        :async:

        Flattens all the elements in this iterator into a list.

        Returns
        --------
        :class:`list`
            A list of every element in the async iterator.

    .. method:: map(func)
        
        Similar to Python's built-in ``map`` function.
        This returns a new iterator that executes ``func`` on every element that it is iterating over.

        ``func`` can either be a normal function or a coroutine.

    .. method:: filter(func)
        
        Similar to Python's built-in ``filter`` function.
        This returns a new iterator that filters over the original iterator.

        ``func`` can either be a normal function or a coroutine.


Exceptions
-----------
.. automodule:: nhentaio.errors
   :members:

.. autoclass:: nhentaio.NoMoreItems
