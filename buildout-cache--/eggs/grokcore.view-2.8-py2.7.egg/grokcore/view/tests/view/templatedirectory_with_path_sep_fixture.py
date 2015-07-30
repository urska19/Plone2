"""
This should fail because you can not use path separator in templatedir directive.
"""
import grokcore.view as grok
import os.path

grok.templatedir('templatedirectoryname' + os.path.sep + 'subdirname')
