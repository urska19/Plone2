Tests related to getting terms from registry
============================================

Some example content and vocabularies

    >>> context = layer.context
    >>> example_vocab = layer.example_vocab
    >>> example_source = layer.example_source
    >>> [i.value for i in example_vocab]
    [1, 2, 3, 4]

    >>> from collective.elephantvocabulary import wrap_vocabulary

    >>> wrapped_vocab_factory = wrap_vocabulary(example_vocab,
    ...         hidden_terms_from_registry='example.hidden_terms')

    >>> wrapped_vocab1 = wrapped_vocab_factory(context)

Hidden terms should not grow after instanciating the vocab factory several
times:

    >>> wrapped_vocab_factory.hidden_terms
    [1, 2]

    >>> wrapped_vocab2 = wrapped_vocab_factory(context)

    >>> wrapped_vocab_factory.hidden_terms
    [1, 2]


Same for visible terms - visible terms should not grow after instanciating the
vocab factory several times:


    >>> wrapped_vocab_factory = wrap_vocabulary(example_vocab,
    ...         visible_terms_from_registry='example.visible_terms')

    >>> wrapped_vocab1 = wrapped_vocab_factory(context)


    >>> wrapped_vocab_factory.visible_terms
    [1, 2, 3]

    >>> wrapped_vocab2 = wrapped_vocab_factory(context)

    >>> wrapped_vocab_factory.visible_terms
    [1, 2, 3]
