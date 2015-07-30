"""
Templates that are not associated with a view class will provoke an
error:

  >>> from grokcore.view.testing import warn
  >>> import warnings
  >>> saved_warn = warnings.warn
  >>> warnings.warn = warn

  >>> grok.testing.grok(__name__)
  From grok.testing's warn():
  ...UserWarning: Found the following unassociated template after configuration:
  ...unassociated_templates...index.pt...

Also templates of modules named equally as the package name the module
resides in, should be found without error or warning. We check this
with the local package `modequalspkgname`::

  >>> warnings.warn = warn

  >>> pkg = __name__.rsplit('.', 1)[0] + '.modequalspkgname'
  >>> grok.testing.grok(pkg) is None
  True

  >>> warnings.warn = saved_warn

"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass
