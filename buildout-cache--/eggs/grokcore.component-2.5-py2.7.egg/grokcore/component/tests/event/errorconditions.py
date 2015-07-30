"""
@grok.subscribe can only be used on module level:

  >>> function_context()
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.subscribe can only be used on module level.
  
  >>> class_context()
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.subscribe can only be used on module level.


@grok.subscribe can not be called without arguments:

  >>> import grokcore.component.tests.event.errorconditions_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.subscribe requires at least one argument.
  
"""
import grokcore.component as grok
from zope.component.interfaces import IObjectEvent

def function_context():
    @grok.subscribe(grok.Context, IObjectEvent)
    def subscriber():
        pass
    
def class_context():
    class Wrapper:
        @grok.subscribe(grok.Context, IObjectEvent)
        def subscriber(self):
            pass
