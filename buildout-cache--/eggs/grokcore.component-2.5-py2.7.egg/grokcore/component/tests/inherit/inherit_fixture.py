import grokcore.component
from zope.interface import Interface

class Foo(grokcore.component.Context):
    pass

grokcore.component.context(Foo)

class IAnder(Interface):
    pass

class FooAdapter(grokcore.component.Adapter):
    grokcore.component.provides(IAnder)

