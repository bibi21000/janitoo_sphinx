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

from janitoo_sphinx.base import EXT_TYPES
from janitoo_sphinx.base import JanitooDirective
from janitoo_sphinx.base import convert_to_list

class PackageDirective(JanitooDirective):
    """ Package directive.

    Injects Janitoo's package informations in the documentation.

    Usage, in a sphinx documentation :

        .. jnt-package::
            :infos: name, desc, fulldesc, tags, ... of the Janitoo package. minimal and full are group of infos. If not set, show minimal (name + desc) informations.

    """
    has_content = True
    option_spec = {
            'types': convert_to_list,
        }
    doc_field_types = []

    def run(self):
        """
        """
        jtypes = self.options.get('types', EXT_TYPES)
        entry = self.options.get('entry', None)
        package = self._get_package()
        pkg_map = {
            'components' : {
                    'callback' : package.get_janitoo_components,
                    'title' : 'Components',
            },
            'threads' : {
                    'callback' : package.get_janitoo_threads,
                    'title' : 'Threads (bus)',
            },
            'bus' : {
                    'callback' : package.get_janitoo_bus_extensions,
                    'title' : 'Bus extensions',
            },
            'values' : {
                    'callback' : package.get_janitoo_values,
                    'title' : 'Values in factory',
            },
            'models' : {
                    'callback' : package.get_janitoo_models,
                    'title' : 'Database Models',
            },
        }

        datas = {}
        for jtype in jtypes:
            data = pkg_map[jtype]['callback']()
            if len(data) > 0:
                if entry is None:
                    datas[jtype] = { 'datas' : data, 'title' : pkg_map[jtype]['title']}
                else:
                    for item in data:
                        if item == entry:
                            datas[jtype] = { 'datas' : {item : data[item]}, 'title' : pkg_map[jtype]['title']}

        return [self._render_type(datas, s) for s in datas.keys()]

    def _render_type(self, datas, jtype):
        """
        """
        jtype_id = "type-%d" % self.env.new_serialno('jtype')
        jtype_node = nodes.section(ids=[jtype_id])

        title = '%s' % (datas[jtype]['title'])
        jtype_node += nodes.title(text=title)

        for data in sorted(datas[jtype]['datas'].keys()):
            item = nodes.list_item()
            item += [
                nodes.strong(text=six.text_type(data)),
                nodes.inline(text=" : "),
                nodes.emphasis(text=six.text_type(datas[jtype]['datas'][data])),
            ]
            jtype_node.append(item)

        return jtype_node
