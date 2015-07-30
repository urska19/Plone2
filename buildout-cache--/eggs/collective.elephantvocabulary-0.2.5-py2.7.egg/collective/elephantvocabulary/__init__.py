from collective.elephantvocabulary.vocabulary import VocabularyFactory
from collective.elephantvocabulary.hidden import WrapperHidden
from collective.elephantvocabulary.visible import WrapperVisible
from collective.elephantvocabulary.base import WrapperBase


def wrap_vocabulary(vocab,
                    visible_terms=None,
                    visible_terms_from_registry=None,
                    hidden_terms=None,
                    hidden_terms_from_registry=None,
                    wrapper_class=WrapperBase):
    return VocabularyFactory(
        vocab,
        visible_terms=visible_terms,
        visible_terms_from_registry=visible_terms_from_registry,
        hidden_terms=hidden_terms,
        hidden_terms_from_registry=hidden_terms_from_registry,
        wrapper_class=WrapperBase,
    )


__all__ = ['wrap_vocabulary', 'WrapperBase', 'WrapperVisible', 'WrapperHidden']
