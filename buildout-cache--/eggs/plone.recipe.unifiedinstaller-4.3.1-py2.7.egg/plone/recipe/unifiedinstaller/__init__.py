import os
import zc.buildout
import zc.recipe.egg


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


class Recipe:

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.options, self.name = buildout, options, name

        # logging.getLogger(self.name).info(buildout['buildout'])

        self._location = buildout['buildout']['directory']
        self._bin_directory = buildout['buildout']['bin-directory']
        self._parts_directory = buildout['buildout']['parts-directory']
        self._shell_command = options.get('shell-command', '/bin/sh')
        self._sudo_command = options.get('sudo-command', 'SUDOXXX')
        self._start_command = options.get('start-command', 'plonectl start')
        self._stop_command = options.get('stop-command', 'plonectl stop')
        self._user = options.get('user', '')
        self._effective_user = options.get('effective-user', '')
        self._buildout_user = options.get('buildout-user', '')
        self._need_sudo = options.get('need-sudo', 'false').lower() in ('true', 'yes', 'on')

        # options['scripts'] = ''  # suppress script generation.

        file_storage = options.get('file-storage', os.path.join(self._location, 'var', 'filestorage', 'Data.fs'))
        file_storage = os.path.join(self._location, file_storage)
        self._fileStorage = file_storage
        self._fileStorageDir = os.path.dirname(file_storage)

    def install(self):
        options = self.options

        buildout_parts = self.buildout['buildout'].get('parts', '').split()

        self._zeoserver = options.get('zeoserver')
        if self._zeoserver is None:
            # look for server definitions in the buildout
            servers = \
                [part for part in buildout_parts
                 if self.buildout[part].get('recipe', '')
                    in ('plone.recipe.zope2zeoserver', 'plone.recipe.zeoserver')
                ]
            if len(servers) == 1:
                self._zeoserver = servers[0]

        self._clients = options.get('clients')
        if self._clients is None:
            # look for client definitions in the buildout
            clients = [
                part for part in buildout_parts
                if self.buildout[part].get('recipe', '') == 'plone.recipe.zope2instance'
                ]
            self._clients = '\n'.join(clients)

        # let's find a client port that we can use in the README
        client_ports = [
            self.buildout[part].get('http-address')
            for part in clients
            ]
        if client_ports and client_ports[0]:
            self._primary_port = client_ports[0]
        else:
            self._primary_port = options.get('port')

        paths = [self.writeTemplate('admin_text', 'adminPassword.txt')]
        os.chmod(paths[0], 0600)

        self.writeTemplate('parts_readme_text',
            os.path.join(self._location, self._parts_directory, 'README.txt')
            )
        paths.append('%s/README.txt' % self._parts_directory)

        self.writeTemplate('readme_html', 'README.html')
        paths.append('README.html')

        requirements, ws = self.egg.working_set(['plone.recipe.unifiedinstaller'])
        zc.buildout.easy_install.scripts(
            [('plonectl',
                'plone.recipe.unifiedinstaller.ctl', 'main')],
            ws, options['executable'], options['bin-directory'],
            extra_paths=[],
            arguments=(
                """server=%s, clients=%s, location=r'%s', binDirectory=r'%s', fileStorage=r'%s'""" % \
                    (`self._zeoserver`,
                     self._clients.split(),
                     self._location,
                     self._bin_directory,
                     self._fileStorage)
                ),
            )

        return paths

    def update(self):
        return self.install()

    def writeTemplate(self, template, filename):
        sudo_eu = ''
        sudo_bu = ''
        if self._need_sudo:
            sudo_eu = "sudo -u %s" % self._effective_user
            sudo_bu = "sudo -u %s" % self._buildout_user
        options = self.options
        script = read(template) % dict(
          bin_dir=self._bin_directory,
          location=self._location,
          zeoserver=options.get('zeoserver', ''),
          clients=' '.join(options.get('clients', '').split()),
          shell_cmd=self._shell_command,
          start_cmd=self._start_command,
          stop_cmd=self._stop_command,
          password=self._user.split(':')[1],
          user=self._user.split(':')[0],
          port=self._primary_port,
          sudo_effective_user=sudo_eu,
          sudo_buildout_user=sudo_bu,
          file_storage=self._fileStorage,
          file_storage_dir=self._fileStorageDir,
          )

        open(filename, 'w').write(script)

        return filename
