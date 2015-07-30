
from collective.elephantvocabulary.base import WrapperBase


class WrapperHidden(WrapperBase):

    def __init__(self, vocab, hidden_terms=None):
        super(WrapperHidden, self).__init__(vocab, None, hidden_terms)
