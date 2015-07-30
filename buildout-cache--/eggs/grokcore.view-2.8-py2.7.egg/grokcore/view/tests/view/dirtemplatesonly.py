"""
A template directory may only contain recognized template files::

  >>> from grokcore.view.testing import warn, lastwarning
  >>> import warnings
  >>> saved_warn = warnings.warn
  >>> warnings.warn = warn

  >>> grok.testing.grok(__name__)
  From grok.testing's warn():
  ... UserWarning: File 'invalid.txt' has an unrecognized extension in
  directory '...dirtemplatesonly_templates'...

Files ending with '.cache' are generated on the fly by some template
engines. Although they provide no valid template filename extension,
they are ignored.

There is a 'template' ``ignored.cache`` in our template dir, which
emits no warning::

  >>> 'ignored.cache' in lastwarning
  False

The same applies to files and directories ending with '~' or starting
with a dot ('.').

Restore the warning machinery::

  >>> warnings.warn = saved_warn

"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class Index(grok.View):
    pass
