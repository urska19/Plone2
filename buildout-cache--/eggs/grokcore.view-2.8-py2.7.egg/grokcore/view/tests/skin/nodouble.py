"""
We cannot register two skins under the same name::

    >>> from grokcore.view.tests.skin import nodouble_fixture
    Traceback (most recent call last):
    ...
    GrokImportError: The 'skin' directive can only be called once per class.

"""
