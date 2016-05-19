# -*- coding: utf-8 -*-
""" http://www.sphinx-doc.org/en/stable/extdev/tutorial.html
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

import sys

from datetime import datetime
import re

import six
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from janitoo_packaging import packaging

class JanitooDirectiveBase(Directive):
    """
    """
    has_content = True

    def _get_package(self):
        """
        """
        env = self.state.document.settings.env
        package = packaging.Package(setuppy='setup', directory="../..")
        return package

    def _populate_extension(self, datas, target):
        """
        """
        for data in datas:
            item = nodes.list_item()
            item += [
                nodes.strong(text=six.text_type(data)),
                nodes.inline(text=" : "),
                nodes.emphasis(text=six.text_type(datas[data])),
            ]
            target.append(item)

        env = self.state.document.settings.env
        package = packaging.Package(setuppy='setup', directory="../..")
        return package


class JanitooExtensions(JanitooDirectiveBase):
    """
    """
    option_spec = {
            'models': bool,
            'threads': bool,
            'components': bool,
            'busexts': bool,
            'values': bool,
            'all': bool,
        }

    def run(self):
        """
        """
        self.package = self._get_package()
        markup = self._build_markup()
        return markup

    def _build_markup(self):
        """
        """
        field_list = nodes.field_list()
        item = nodes.paragraph()
        item.append(field_list)
        if 'threads' in self.options or 'all' in self.options:
            name = nodes.field_name(text="Threads")
            body = nodes.field_body()
            body.append(nodes.emphasis(text=six.text_type("Some text")))
            field = nodes.field()
            field += [name, body]
            field_list.append(field)
            self._populate_extension(self.package.get_janitoo_threads(), field_list)
        if 'values' in self.options or 'all' in self.options:
            self._populate_extension(self.package.get_janitoo_values(), field_list)
        return [item]

def setup(app):
    """
    """
    app.add_directive('janitoo_extensions', JanitooExtensions)
