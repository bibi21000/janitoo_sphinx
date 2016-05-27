#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file of Janitoo
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

from os import name as os_name
from setuptools import setup, find_packages
from distutils.extension import Extension
from platform import system as platform_system
import glob
import os
import sys
from _version import janitoo_version

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

def data_files_config(res, rsrc, src, pattern):
    for root, dirs, fils in os.walk(src):
        if src == root:
            sub = []
            for fil in fils:
                sub.append(os.path.join(root,fil))
            res.append((rsrc, sub))
            for dire in dirs:
                    data_files_config(res, os.path.join(rsrc, dire), os.path.join(root, dire), pattern)

#~ data_files = []
#~ data_files_config(data_files, 'docs','src/docs/','*')
#~
#~ janitoo_entry_points = {
    #~ "janitoo.threads": [
        #~ "fake = janitoo.tests:make_thread",
    #~ ],
    #~ "janitoo.components": [
        #~ "fake.component = janitoo.tests:make_fake_component",
    #~ ],
#~ }

setup(
    name = 'janitoo_sphinx',
    description = "Sphinx contribution for Janitoo",
    long_description = "A collection of Sphinx contributions to help writing documentation for Janitoo.",
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    license = """
        This file is part of Janitoo.

        Janitoo is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Janitoo is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Janitoo. If not, see <http://www.gnu.org/licenses/>.
    """,
    url='http://bibi21000.gallet.info/',
    version = janitoo_version,
    zip_safe = False,
    packages = find_packages('src', exclude=["scripts", "docs", "config"]),
    include_package_data=True,
    package_dir = { '': 'src' },
    keywords = "documentation",
    install_requires=[
                     'pygraphviz',
                     'rst2pdf',
                     'sphinxcontrib-blockdiag',
                     'sphinxcontrib-seqdiag',
                     'sphinxcontrib-actdiag',
                     'sphinxcontrib-nwdiag',
                     'sphinxcontrib-autoprogram',
                     'sphinxcontrib-programoutput',
                     'sphinxcontrib-spelling',
                     'sphinxcontrib-images',
                     'sphinxcontrib-restbuilder',
                     'sphinxcontrib-jinjadomain',
                     'sphinxcontrib-httpdomain',
                     'sphinx_bootstrap_theme',
                     #~ 'sphinx-git',
                    ],
    #~ tests_require=['janitoo_nosetests'],
    dependency_links = [
      'https://github.com/OddBloke/sphinx-git.git',
    ],
    #~ entry_points = janitoo_entry_points,
)