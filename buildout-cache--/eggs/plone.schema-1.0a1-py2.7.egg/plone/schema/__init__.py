from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone.schema')


from .email import Email
from .email import IEmail

from .path import Path
from .path import IPath

# zope.schema convenience imports
from zope.schema._field import ASCII
from zope.schema._field import ASCIILine
from zope.schema._field import Bool
from zope.schema._field import Bytes
from zope.schema._field import BytesLine
from zope.schema._field import Choice
from zope.schema._field import Container
from zope.schema._field import Date
from zope.schema._field import Datetime
from zope.schema._field import Decimal
from zope.schema._field import Dict
from zope.schema._field import DottedName
from zope.schema._field import Field
from zope.schema._field import Float
from zope.schema._field import FrozenSet
from zope.schema._field import Id
from zope.schema._field import Int
from zope.schema._field import InterfaceField
from zope.schema._field import Iterable
from zope.schema._field import List
from zope.schema._field import MinMaxLen
from zope.schema._field import NativeString
from zope.schema._field import NativeStringLine
from zope.schema._field import Object
from zope.schema._field import Orderable
from zope.schema._field import Password
from zope.schema._field import Set
from zope.schema._field import SourceText
from zope.schema._field import Text
from zope.schema._field import TextLine
from zope.schema._field import Time
from zope.schema._field import Timedelta
from zope.schema._field import Tuple
from zope.schema._field import URI
