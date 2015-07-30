import grokcore.view

class DirectoryResourceFoo(grokcore.view.DirectoryResource):
    grokcore.view.name('foo')
    grokcore.view.path('foo')

class DirectoryResourceBaz(grokcore.view.DirectoryResource):
    grokcore.view.name('baz')
    grokcore.view.path('bar/baz')
