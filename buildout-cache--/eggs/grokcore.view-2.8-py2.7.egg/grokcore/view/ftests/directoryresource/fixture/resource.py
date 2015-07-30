import os
import grokcore.view

class DirectoryResourceFoo(grokcore.view.DirectoryResource):
    grokcore.view.path('foo')

class IAnotherLayer(grokcore.view.IDefaultBrowserLayer):
    grokcore.view.skin('another')

class DirectoryResourceFooOnLayer(grokcore.view.DirectoryResource):
    grokcore.view.layer(IAnotherLayer)
    grokcore.view.path('anotherfoo')

class DirectoryResourceBarWithName(grokcore.view.DirectoryResource):
    grokcore.view.name('fropple')
    grokcore.view.path('bar')

class DirectoryResourceBazInsubdirWithName(grokcore.view.DirectoryResource):
    grokcore.view.name('frepple')
    grokcore.view.path('bar/baz')

absolute_path = os.path.join(os.path.dirname(__file__), 'bar', 'baz')

class DirectoryResourceQuxWithNameAbsolutePath(grokcore.view.DirectoryResource):
    grokcore.view.name('frupple')
    grokcore.view.path(absolute_path)
