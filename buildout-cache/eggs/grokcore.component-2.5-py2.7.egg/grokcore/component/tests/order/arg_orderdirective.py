"""
If the grok.order directive is present with arguments, sorting will be
done by the order specified.

  >>> from grokcore.component import sort_components

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...Fourth object at ...>,
   <...Third object at ...>,
   <...Second object at ...>,
   <...First object at ...>]

You can use the key option:

  >>> from operator import itemgetter

  >>> components = [(1, First()), (2, Second()), (3, Third())]
  >>> sort_components(components, key=itemgetter(1))
  [(3, <...Third object at ...>),
   (2, <...Second object at ...>),
   (1, <...First object at ...>)]

"""

import grokcore.component as grok

class First(object):
    grok.order(5)

class Second(object):
    grok.order(4)

class Third(object):
    grok.order(3)

class Fourth(object):
    grok.order(2)

class Fifth(object):
    grok.order(1)
