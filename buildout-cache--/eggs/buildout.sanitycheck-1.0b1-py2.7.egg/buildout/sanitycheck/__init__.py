import logging
import os

from zc.buildout import UserError

disclaimer = \
"""If you have a good reason to bypass this restriction,
remove the buildout.sanitycheck extension from your buildout."""


def check_root(buildout, logger):
    """ Refuse to run as root """

    if os.geteuid() == 0:
        effective_user = buildout['buildout'].get('buildout-user', 'buildout_user')
        logger.error("""
***********************************************************
Buildout should not be run while superuser. Doing so allows
untrusted code to be run as root.
Instead, you probably wish to do something like:
    sudu -u %s bin/buildout

%s
***********************************************************
""" % (effective_user, disclaimer))
        raise UserError('User attempt to give system ownership to Internet')


def main(buildout):
    logger = logging.getLogger("buildout.sanitycheck")
    check_root(buildout, logger)
