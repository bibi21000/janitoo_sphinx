# -*- coding: utf-8 -*-
"""
Sources :

 - http://www.sphinx-doc.org/en/stable/extdev/tutorial.html
 - https://github.com/mozilla-services/cornice/blob/master/cornice/ext/sphinxext.py

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

import logging
#~ logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

import six

from docutils import nodes
from docutils.parsers.rst import directives

from janitoo_sphinx.base import BADG_TYPES
from janitoo_sphinx.base import JanitooDirective
from janitoo_sphinx.base import convert_to_list
import os
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image

class BadgeNode(nodes.image, nodes.General, nodes.Element):
    pass

def visit_badge_node(self, node):
    self.visit_image(node)

def depart_badge_node(self, node):
    self.depart_image(node)

class BadgeDirective(JanitooDirective):

    """ Badges directive.

    Injects Janitoo's badges informations in the documentation.

    Usage, in a sphinx documentation :

        .. jnt-badge::
            :badges: travis, ...

    """
    has_content = True
    option_spec = {
            'badges': convert_to_list,
        }
    doc_field_types = []

    def run(self):
        """
        """
        jbadges = self.options.get('badges', ['travis', 'coversall', 'landscape'])
        package = self._get_package()
        pkg_map = {
            'travis' : {
                    'url' : package.get_travis_url,
                    'badge' : package.get_travis_badge,
                    'alt' : 'Continuous integration',
            },
            'landscape' : {
                    'url' : package.get_landscape_url,
                    'badge' : package.get_landscape_badge,
                    'alt' : 'Health',
            },
            'coversall' : {
                    'url' : package.get_coveralls_url,
                    'badge' : package.get_coveralls_badge,
                    'alt' : 'Coverage',
            },
            'documentation' : {
                    'url' : package.get_doc_url,
                    'badge' : package.get_doc_badge,
                    'alt' : 'Documentation',
            },
            'circle' : {
                    'url' : package.get_circle_url,
                    'badge' : package.get_circle_badge,
                    'alt' : 'Continuous integration',
            },
            'docker' : {
                    'url' : package.get_docker_url,
                    'badge' : package.get_docker_badge,
                    'alt' : 'Docker',
            },
        }
        group = self.options.get('group',
            self.env.config['default_group'] if 'default_group' in self.env.config and self.env.config['default_group'] else self.env.new_serialno('jpackage'))
        datas = {}
        for jbadge in jbadges:
            datas[jbadge] = {
                'target':pkg_map[jbadge]['url'](),
                'badge':pkg_map[jbadge]['badge'](),
                'alt':pkg_map[jbadge]['alt'],
                'group':group,
            }
        return [self._render_badge(datas, s) for s in datas.keys()]


    def _render_badge(self, datas, jbadge):
        """
        """
        img = BadgeNode()
        img['alt'] = datas[jbadge]['alt']
        img['group'] = datas[jbadge]['group']
        img['target'] = datas[jbadge]['target']
        img['uri'] = datas[jbadge]['badge']
        img['title'] = ''
        return img
