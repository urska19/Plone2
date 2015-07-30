"""
This should fail because ``grok.template`` points to a non-existing
template:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  ConfigurationExecutionError: martian.error.GrokError: Template cavepainting for View <class 'grokcore.view.tests.view.templatenotfound.Painting'> cannot be found.
  in:
"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class Painting(grok.View):
    grok.template('cavepainting')

# no cavepainting template here
