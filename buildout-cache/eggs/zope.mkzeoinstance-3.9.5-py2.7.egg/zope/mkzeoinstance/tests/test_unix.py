##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import sys
import unittest
import tempfile
import os
import shutil
import cStringIO

from zope.mkzeoinstance import ZEOInstanceBuilder
from zope.mkzeoinstance import mkdirs
from zope.mkzeoinstance import makedir
from zope.mkzeoinstance import makefile
from zope.mkzeoinstance import makexfile


class ZeoInstanceParamsTest(unittest.TestCase):

    def test_get_params(self):
        builder = ZEOInstanceBuilder()

        params = builder.get_params(zodb3_home='',
                                    zdaemon_home='',
                                    instance_home='',
                                    address='')
        expected_params = {'PACKAGE': 'ZEO',
                           'python': sys.executable,
                           'package': 'zeo',
                           'zdaemon_home': '',
                           'instance_home': '',
                           'address': '',
                           'zodb3_home': ''}

        self.assertEqual(params, expected_params)


class ZeoInstanceCreateTest(unittest.TestCase):

    def setUp(self):
        self.builder = ZEOInstanceBuilder()
        self.temp_dir = tempfile.mkdtemp()

        self.instance_home = os.path.join(self.temp_dir, 'instance')

        import zdaemon
        self.zdaemon_home = os.path.split(zdaemon.__path__[0])[0]

        self.zodb3_home = None
        for entry in sys.path:
            if os.path.exists(os.path.join(entry, 'ZODB')):
                self.zodb3_home = entry
                break

        self.params = {'PACKAGE': 'ZEO',
                       'python': sys.executable,
                       'package': 'zeo',
                       'zdaemon_home': self.zdaemon_home,
                       'instance_home': self.instance_home,
                       'address': '99999',
                       'zodb3_home': self.zodb3_home}

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_folders_and_files(self):
        instance_home = self.instance_home
        orig_stdout = sys.stdout

        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        self.builder.create(instance_home, self.params)
        sys.stdout = orig_stdout

        expected_out = """Created directory %(instance_home)s
Created directory %(instance_home)s/etc
Created directory %(instance_home)s/var
Created directory %(instance_home)s/log
Created directory %(instance_home)s/bin
Wrote file %(instance_home)s/etc/zeo.conf
Wrote file %(instance_home)s/bin/zeoctl
Changed mode for %(instance_home)s/bin/zeoctl to 755
Wrote file %(instance_home)s/bin/runzeo
Changed mode for %(instance_home)s/bin/runzeo to 755
""" % {'instance_home':
           instance_home}

        self.assertEqual(temp_out_file.getvalue(), expected_out)

        self.assertTrue(os.path.exists(os.path.join(instance_home, 'etc')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'var')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'log')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'bin')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'etc', 'zeo.conf')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'bin', 'zeoctl')))
        self.assertTrue(os.path.exists(os.path.join(instance_home, 'bin', 'runzeo')))

    def test_zeo_conf_content(self):
        instance_home = self.instance_home
        orig_stdout = sys.stdout

        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        self.builder.create(instance_home, self.params)
        sys.stdout = orig_stdout
        zeo_conf_path = os.path.join(instance_home, 'etc', 'zeo.conf')
        zeo_conf = open(zeo_conf_path).read()
        expected_out = """# ZEO configuration file

%%define INSTANCE %(instance_home)s

<zeo>
  address 99999
  read-only false
  invalidation-queue-size 100
  # pid-filename $INSTANCE/var/ZEO.pid
  # monitor-address PORT
  # transaction-timeout SECONDS
</zeo>

<filestorage 1>
  path $INSTANCE/var/Data.fs
</filestorage>

<eventlog>
  level info
  <logfile>
    path $INSTANCE/log/zeo.log
  </logfile>
</eventlog>

<runner>
  program $INSTANCE/bin/runzeo
  socket-name $INSTANCE/var/zeo.zdsock
  daemon true
  forever false
  backoff-limit 10
  exit-codes 0, 2
  directory $INSTANCE
  default-to-interactive true
  # user zope
  python %(executable)s
  zdrun %(zdaemon_home)s/zdaemon/zdrun.py

  # This logfile should match the one in the zeo.conf file.
  # It is used by zdctl's logtail command, zdrun/zdctl doesn't write it.
  logfile $INSTANCE/log/zeo.log
</runner>
""" % {'instance_home': self.instance_home,
       'executable': sys.executable,
       'zdaemon_home': self.zdaemon_home}

        self.assertEqual(zeo_conf, expected_out)

    def test_zeoctl_content(self):
        instance_home = self.instance_home
        orig_stdout = sys.stdout

        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        self.builder.create(instance_home, self.params)
        sys.stdout = orig_stdout
        zeoctl_path = os.path.join(instance_home, 'bin', 'zeoctl')
        zeoctl = open(zeoctl_path).read()
        expected_out = """#!/bin/sh
# ZEO instance control script

# The following two lines are for chkconfig.  On Red Hat Linux (and
# some other systems), you can copy or symlink this script into
# /etc/rc.d/init.d/ and then use chkconfig(8) to automatically start
# ZEO at boot time.

# chkconfig: 345 90 10
# description: start a ZEO server

PYTHON="%(executable)s"
INSTANCE_HOME="%(instance_home)s"
ZODB3_HOME="%(zodb3_home)s"

CONFIG_FILE="%(instance_home)s/etc/zeo.conf"

PYTHONPATH="$ZODB3_HOME"
export PYTHONPATH INSTANCE_HOME

ZEOCTL="$ZODB3_HOME/ZEO/zeoctl.py"

exec "$PYTHON" "$ZEOCTL" -C "$CONFIG_FILE" ${1+"$@"}
""" % {'zodb3_home': self.zodb3_home,
       'instance_home': self.instance_home,
       'executable': sys.executable}

        self.assertEqual(zeoctl, expected_out)


class UtilityFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_mkdirs(self):
        path = os.path.join(self.temp_dir, 'test')
        orig_stdout = sys.stdout
        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        mkdirs(path)
        sys.stdout = orig_stdout
        self.assertEqual('Created directory %s\n'%path,
                         temp_out_file.getvalue())
        self.assertTrue(os.path.exists(path))

    def test_makedir(self):
        path = os.path.join(self.temp_dir, 'test')
        orig_stdout = sys.stdout
        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        makedir(self.temp_dir, 'test')
        sys.stdout = orig_stdout
        self.assertEqual('Created directory %s\n'%path,
                         temp_out_file.getvalue())
        self.assertTrue(os.path.exists(path))

    def test_makefile(self):
        template = "KEY=%(key)s"
        params = {'key': 'value'}

        orig_stdout = sys.stdout
        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        makefile(template, self.temp_dir, 'test.txt', **params)
        sys.stdout = orig_stdout
        path = os.path.join(self.temp_dir, 'test.txt')
        self.assertEqual('Wrote file %s\n'%path,
                         temp_out_file.getvalue())

        self.assertEqual('KEY=value',
                         open(path).read())

    def test_makexfile(self):
        orig_stdout = sys.stdout
        temp_out_file = cStringIO.StringIO()
        sys.stdout = temp_out_file
        params = {}
        makexfile('', self.temp_dir, 'test.txt', **params)
        sys.stdout = orig_stdout
        path = os.path.join(self.temp_dir, 'test.txt')
        expected_out = """Wrote file %(path)s
Changed mode for %(path)s to 755\n"""
        self.assertEqual(expected_out%{'path':path},
                         temp_out_file.getvalue())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZeoInstanceParamsTest))
    suite.addTest(unittest.makeSuite(ZeoInstanceCreateTest))
    suite.addTest(unittest.makeSuite(UtilityFunctionsTest))
    return suite
