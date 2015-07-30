Usage
=====

Some example content and vocabularies

    >>> context = layer.context
    >>> example_vocab = layer.example_vocab
    >>> example_source = layer.example_source
    >>> [i.value for i in example_vocab]
    [1, 2, 3, 4]

Below is out wraper method we use to make our existing vocab more
elephant-like.

    >>> from collective.elephantvocabulary import wrap_vocabulary

In first exampe we pass to our ``wrap_vocabulary`` a vocabulary of
[1, 2, 3, 4] and we set terms 2 and 3 to hidden. ``wrap_vocabulary``
returns ``VocabularyFactory`` which needs to be called with context
(you could also register it with as utility).

    >>> wrapped_vocab_factory = wrap_vocabulary(example_vocab, hidden_terms=[2, 3])
    >>> print wrapped_vocab_factory
    <collective.elephantvocabulary.vocabulary.VocabularyFactory object at ...>

    >>> wrapped_vocab = wrapped_vocab_factory(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 4]

    >>> len(wrapped_vocab) == len(example_vocab)
    True

    >>> 2 in wrapped_vocab
    True

    >>> 5 in wrapped_vocab
    False

    >>> wrapped_vocab.getTerm(3).value
    3

Similar we can limit items shown only to the set we want (via
``visible_terms``)

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 visible_terms=[2, 3])(context)
    >>> [i.value for i in wrapped_vocab]
    [2, 3]

    >>> len(wrapped_vocab) == len(example_vocab)
    True

    >>> 2 in wrapped_vocab
    True

    >>> 5 in wrapped_vocab
    False

    >>> wrapped_vocab.getTerm(1).value
    1

Above we see what ``collective.elephantvocabulary`` is all about. When listing
vocabulary hidden terms are not listed. But when item is requested with its
term value then term is also returned. Also length of vocabulary is unchanged.
It still shows original lenght of vocabulary.

We can also call vocabulary by name it was register with ZCA machinery..

    >>> wrapped_vocab = wrap_vocabulary('example-vocab',
    ...                                  hidden_terms=[2, 3])(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 4]

``hidden_terms`` or ``visible_terms`` parameter (second argument we pass to
``wrap_vocabulary``) can also be callable which expects 2 parameters,
``context`` and ``original vocabulary``.

    >>> def hidden_terms(context, vocab):
    ...     return [1, 4]

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 hidden_terms=hidden_terms)(context)
    >>> [i.value for i in wrapped_vocab]
    [2, 3]

    >>> def visible_terms(context, vocab):
    ...     return [1, 4]

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 visible_terms=hidden_terms)(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 4]

``collective.elephantvocabulary`` also works with sources.

    >>> [i.value for i in example_source]
    [1, 2, 3, 4]

    >>> [i.value for i in example_source.search()]
    [1, 2]

    >>> wrapped_source = wrap_vocabulary(example_source, hidden_terms=[1, 4])(context)
    >>> [i.value for i in wrapped_source.search()]
    [2]

    >>> wrapped_source = wrap_vocabulary(example_source, visible_terms=[1, 4])(context)
    >>> [i.value for i in wrapped_source.search()]
    [1]

If vocabulary already provides set of hidden terms they are passed to wrapped
vocabulary.

    >>> example_vocab.hidden_terms = [1, 2]
    >>> wrapped_vocab = wrap_vocabulary(example_vocab)(context)
    >>> [i.value for i in wrapped_vocab]
    [3, 4]


    >>> del example_vocab.hidden_terms

    >>> example_vocab.visible_terms= [1, 2]
    >>> wrapped_vocab = wrap_vocabulary(example_vocab)(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 2]

    >>> del example_vocab.visible_terms

Vocabulary will ass to the list of passed ``visible_terms`` or ``hidden_terms``.

    >>> example_vocab.hidden_terms = [1, 2]
    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 hidden_terms=[2, 3])(context)
    >>> [i.value for i in wrapped_vocab]
    [4]


    >>> del example_vocab.hidden_terms

    >>> example_vocab.visible_terms= [1]
    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 visible_terms=[1, 2, 3])(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 2, 3]

    >>> del example_vocab.visible_terms

``hidden_terms`` and ``visible_terms`` can also work together.

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...                                 visible_terms=[1, 2, 3],
    ...                                 hidden_terms=[2])(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 3]

We could also store ``hidden_terms`` and ``visible_terms`` in
`plone.registry`_. Instead of creating our own methods which reads from
plone.registry ``collective.elephantvocabulary`` provides helper parameters:
``hidden_terms_from_registry`` and ``visible_terms_from_registry``.

    >>> from zope.component import getUtility
    >>> from plone.registry import field
    >>> from plone.registry import Record
    >>> from plone.registry.interfaces import IRegistry

    >>> example_registry_record = Record(
    ...         field.List(title=u"Test", min_length=0, max_length=10,
    ...                    value_type=field.Int(title=u"Value")))
    >>> example_registry_record.value = [1, 2]

    >>> registry = getUtility(IRegistry)
    >>> registry.records['example.hidden_terms'] = example_registry_record
    >>> registry.records['example.visible_terms'] = example_registry_record

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...         visible_terms_from_registry='example.visible_terms')(context)
    >>> [i.value for i in wrapped_vocab]
    [1, 2]

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...         hidden_terms_from_registry='example.hidden_terms')(context)
    >>> [i.value for i in wrapped_vocab]
    [3, 4]

Or we can use them in combination.

    >>> example_registry_record2 = Record(
    ...         field.List(title=u"Test", min_length=0, max_length=10,
    ...                    value_type=field.Int(title=u"Value")))
    >>> example_registry_record2.value = [1, 2, 3]
    >>> registry.records['example.visible_terms'] = example_registry_record2

    >>> wrapped_vocab = wrap_vocabulary(example_vocab,
    ...         visible_terms_from_registry='example.visible_terms',
    ...         hidden_terms_from_registry='example.hidden_terms')(context)
    >>> [i.value for i in wrapped_vocab]
    [3]

And if we don't pass anything to ``wrap_vocabulary`` then it should ack as
normal vocabulary.

    >>> wrapped_vocab5 = wrap_vocabulary(example_vocab)(context)
    >>> [i.value for i in wrapped_vocab5]
    [1, 2, 3, 4]

.. _`plone.registry`: http://pypi.python.org/pypi/plone.registry
