# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
from setuptools import setup, find_packages

if __name__ == '__main__':
    print('Sopel does not correctly load modules installed with setup.py '
          'directly. Please use "pip install .", or add {}/sopel_modules to '
          'core.extra in your config.'.format(
              os.path.dirname(os.path.abspath(__file__))),
          file=sys.stderr)

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('NEWS') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = [req for req in requirements_file.readlines()]

with open('dev-requirements.txt') as dev_requirements_file:
    dev_requirements = [req for req in dev_requirements_file.readlines()]

pipcommand = "sudo pip3 install --upgrade"
pipcommand += " --force-reinstall"
pipcommand += " git+https://github.com/sopel-irc/sopel@master"

print('Running {} '.format(pipcommand), file=sys.stderr)
for line in os.popen(pipcommand).read().split('\n'):
    print(line, file=sys.stderr)

import sopel

# Remove stock modules, if present
main_sopel_dir = os.path.dirname(os.path.abspath(sopel.__file__))
modules_dir = os.path.join(main_sopel_dir, 'modules')
stockdir = os.path.join(modules_dir, "stock")
if not os.path.exists(stockdir) or not os.path.isdir(stockdir):
    os.system("sudo mkdir " + stockdir)
for pathname in os.listdir(modules_dir):
    path = os.path.join(modules_dir, pathname)
    if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
        os.system("sudo mv " + path + " " + stockdir)


setup(
    name='sopel_modules.SpiceBot',
    version='0.1.1',
    description='SpiceBot aims to run SpiceBot as an IRC service',
    long_description=readme + '\n\n' + history,
    author='Sam Zick',
    author_email='sam@deathbybandaid.net',
    url='https://github.com/SpiceBot/SpiceBot',
    packages=find_packages('.'),
    namespace_packages=['sopel_modules'],
    include_package_data=True,
    install_requires=requirements,
    tests_require=dev_requirements,
    test_suite='tests',
    license='Eiffel Forum License, version 2',
)
