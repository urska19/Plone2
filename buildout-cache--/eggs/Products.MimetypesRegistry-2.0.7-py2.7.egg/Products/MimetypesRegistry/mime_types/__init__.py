import mtr_mimetypes
import py_mimetypes
import smi_mimetypes
import suppl_mimetypes

from mtr_mimetypes import *


def initialize(registry):
    smi_mimetypes.initialize(registry)
    mtr_mimetypes.initialize(registry)
    suppl_mimetypes.initialize(registry)
    py_mimetypes.initialize(registry)
