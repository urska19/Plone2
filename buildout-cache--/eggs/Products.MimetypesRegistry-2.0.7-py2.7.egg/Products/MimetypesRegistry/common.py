from AccessControl import ModuleSecurityInfo
from types import StringType
from types import UnicodeType
import logging
import os.path


STRING_TYPES = (UnicodeType, StringType)
# directory where template for the ZMI are located
_www = os.path.join(os.path.dirname(__file__), 'www')

security = ModuleSecurityInfo()
security.declarePrivate('logging')
security.declarePrivate('os')
security.declarePrivate('time')

logger = logging.getLogger('MimetypesRegistry')


def log(msg, severity=logging.INFO, id='MimetypesRegistry'):
    logger.log(severity, msg)


class MimeTypeException(Exception):
    pass
