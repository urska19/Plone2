
from zope.interface import implements
from collective.elephantvocabulary.interfaces import IElephantVocabulary
from zope.schema.interfaces import ISource
from zope.schema.interfaces import IIterableSource
from zope.schema.interfaces import IVocabulary


class WrapperBase(object):

    implements(IElephantVocabulary, IVocabulary, ISource, IIterableSource)

    def __init__(self, vocab, visible_terms, hidden_terms):
        self.vocab = vocab
        self.visible_terms = visible_terms
        self.hidden_terms = hidden_terms

    def __contains__(self, name):
        return getattr(self.vocab, '__contains__')(name)

    def __getattr__(self, name):
        return getattr(self.vocab, name)

    def __len__(self):
        return len(self.vocab)

    def _wrap_vocab(self, vocab):
        for term in vocab:
            if self.visible_terms is None and self.hidden_terms is None:
                yield term
            elif self.visible_terms is None and \
                    self.hidden_terms is not None and \
                    term.value not in self.hidden_terms:
                yield term
            elif self.visible_terms is not None and \
                    self.hidden_terms is None and \
                    term.value in self.visible_terms:
                yield term
            elif self.visible_terms is not None and \
                    self.hidden_terms is not None and \
                    term.value in self.visible_terms and \
                    term.value not in self.hidden_terms:
                yield term

    def search(self, *args, **kw):
        return self._wrap_vocab(self.vocab.search(*args, **kw))

    def __iter__(self):
        return self._wrap_vocab(self.vocab)
