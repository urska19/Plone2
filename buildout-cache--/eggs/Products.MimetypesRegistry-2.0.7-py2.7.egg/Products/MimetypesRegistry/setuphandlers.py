from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import logging

logger = logging.getLogger('MimetypesRegistry')


def fixUpSMIGlobs(portal, out=None, reinit=True):
    # This method is used both in migrations where we need the reinit and
    # during site creation, where the registry has already been initialized.
    from Products.MimetypesRegistry.mime_types import smi_mimetypes
    mtr = getToolByName(portal, 'mimetypes_registry')
    if reinit:
        smi_mimetypes.initialize(mtr)

    # Now comes the fun part. For every glob, lookup a extension
    # matching the glob and unregister it.
    for glob in mtr.globs.keys():
        if glob in mtr.extensions:
            logger.debug(
                'Found glob %s in extensions registry, removing.' % glob)
            mti = mtr.extensions[glob]
            del mtr.extensions[glob]
            if glob in mti.extensions:
                logger.debug('Found glob %s in mimetype %s extensions, '
                             'removing.' % (glob, mti))
                exts = list(mti.extensions)
                exts.remove(glob)
                mti.extensions = tuple(exts)
                mtr.register(mti)


def installMimetypesRegistry(portal):
    out = StringIO()
    fixUpSMIGlobs(portal, out, reinit=False)


def setupMimetypesRegistry(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('mimetypes-registry-various.txt') is None:
        return
    site = context.getSite()
    installMimetypesRegistry(site)
