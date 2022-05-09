import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.LegalServerFileExporter',
      version='0.0.1',
      description=('A docassemble extension.'),
      long_description='# LegalServer File Exporter\r\nThis package can be used to download all the documents associated with a LegalServer Case/Matter.\r\n\r\n## Docassemble Server Setup\r\nIn your configuration file, you will need to store your login information for a LegalServer API call. The format should be as follows:\r\n```\r\nlegalserver:\r\n  site_name:\r\n    username: username\r\n    password: password\r\n```\r\nWhere `site_name` is the legalserver site abbreviation (like `demo4-demo`) and the username/password are for an account that has Reports API access. Specifically, the `Login`, `API Access`, and `API Basic Case Information` permissions are needed. \r\n\r\n## Change Log\r\n* 0.0.1 - Initial MVP\r\n',
      long_description_content_type='text/markdown',
      author='Network Ninja, Inc.',
      author_email='mhofrichter@legalserver.org',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/LegalServerFileExporter/', package='docassemble.LegalServerFileExporter'),
     )

