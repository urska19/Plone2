
from collective.elephantvocabulary.base import WrapperBase


class WrapperVisible(WrapperBase):

    def __init__(self, vocab, visible_terms=None):
        super(WrapperVisible, self).__init__(vocab, visible_terms, None)
