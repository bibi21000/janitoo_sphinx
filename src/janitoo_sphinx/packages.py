# -*- coding: utf-8 -*-
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

from janitoo_sphinx.base import JanitooDirective
from janitoo_sphinx.base import convert_to_list

INFO_TYPES = ['title','desc', 'author', 'longdesc', 'keywords', 'license']
"""
Availlable informations
"""

class PackageDirective(JanitooDirective):
    """ Package directive.

    Injects Janitoo's package informations in the documentation.

    Usage, in a sphinx documentation :

    .. code:: bash

        .. jnt-package::
            :infos: desc, longdesc, keywords, ... of the Janitoo package. minimal and full are group of infos. If not set, show minimal (name + desc) informations.

    """
    has_content = True
    option_spec = {
            'infos': convert_to_list,
        }
    doc_field_types = []

    def run(self):
        """
        """
        infos = self.options.get('infos', ['title','desc', 'longdesc'])
        package = self._get_package()

        jpackage_id = "package-%d" % self.env.new_serialno('jpackage')
        jpackage_node = nodes.section(ids=[jpackage_id])

        if 'title' in infos:
            title = '%s' % (package.get_name())
            jpackage_node += nodes.title(text=title)

        if 'desc' in infos:
            jpackage_node.append(
                nodes.paragraph(
                    text=six.text_type(package.get_description())
                )
            )

        if 'author' in infos:
            jpackage_node.append(
                nodes.paragraph(
                    text=six.text_type(package.get_author())
                )
            )

        if 'nickname' in infos:
            jpackage_node.append(
                nodes.paragraph(
                    text=six.text_type(package.get_nickname())
                )
            )

        if 'longdesc' in infos:
            jpackage_node.append(
                nodes.paragraph(
                    text=six.text_type(package.get_long_description())
                )
            )

        if 'license' in infos:
            jpackage_node.append(
                nodes.paragraph(
                    text=six.text_type(package.get_license())
                )
            )

        if 'keywords' in infos:
            for data in sorted(package.get_keywords()):
                item = nodes.list_item()
                item += [
                    nodes.inline(text=six.text_type(data)),
                ]
                jpackage_node.append(item)
            jpackage_node.append(
                nodes.paragraph(
                    text='')
            )
        return [jpackage_node]
