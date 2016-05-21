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

import sys
from datetime import datetime
import re
import json
from importlib import import_module
try:
    from importlib import reload
except ImportError:
    pass
import six

import docutils
from docutils import nodes, core
from docutils.parsers.rst import Directive, directives
from docutils.writers.html4css1 import Writer, HTMLTranslator
from sphinx.util.docfields import DocFieldTransformer

from janitoo_packaging import packaging

EXT_TYPES = [ 'models', 'threads', 'components', 'bus', 'values']
BADG_TYPES = [ 'github', 'githubio', 'travis', 'circle', 'landscape']

def convert_to_list(argument):
    """Convert a comma separated list into a list of python values"""
    if argument is None:
        return []
    else:
        return [i.strip() for i in argument.split(',')]

def convert_to_list_required(argument):
    if argument is None:
        raise ValueError('argument required but none supplied')
    return convert_to_list(argument)

class JanitooDirective(Directive):
    """
    """
    has_content = True
    domain = 'janitoo'

    def __init__(self, *args, **kwargs):
        """
        """
        super(JanitooDirective, self).__init__(*args, **kwargs)
        self.env = self.state.document.settings.env

    def _get_package(self):
        """
        """
        directory="../.."
        if self.env.config.janitoo_source:
            directory = self.env.config.janitoo_source
        package = packaging.Package(setuppy='setup', directory=directory)
        return package

class ExtensionDirective(JanitooDirective):
    """ Extension directive.

    Injects Janitoo's extensions in the documentation.

    Usage, in a sphinx documentation :

        .. jnt-extensions::
            :entry: entry name of the extension. If not set, all extensions are injected.
            :types: types of extension. If not set, all types are injected.

    """
    has_content = True
    option_spec = {
            'entry': directives.unchanged,
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

    def _resolve_obj_to_docstring(self, obj, args):
        """
        """
        # Resolve a view or validator to an object if type string
        # and return docstring.
        if is_string(obj):
            if 'klass' in args:
                ob = args['klass']
                obj_ = getattr(ob, obj.lower())
                return format_docstring(obj_)
            else:
                return ''
        else:
            return format_docstring(obj)

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


# Utils

def format_docstring(obj):
    """Return trimmed docstring with newline from object."""
    return trim(obj.__doc__ or "") + '\n'


def trim(docstring):
    """
    Remove the tabs to spaces, and remove the extra spaces / tabs that are in
    front of the text in docstrings.

    Implementation taken from http://www.python.org/dev/peps/pep-0257/
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    res = '\n'.join(trimmed)
    if not PY3 and not isinstance(res, unicode):
        res = res.decode('utf8')
    return res


class _HTMLFragmentTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['', '', '', '', '']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []

    def astext(self):
        return ''.join(self.body)


class _FragmentWriter(Writer):
    translator_class = _HTMLFragmentTranslator

    def apply_template(self):
        subs = self.interpolation_dict()
        return subs['body']


def rst2html(data):
    """Converts a reStructuredText into its HTML
    """
    if not data:
        return ''
    return core.publish_string(data, writer=_FragmentWriter())


class Env(object):
    temp_data = {}
    docname = ''

def rst2node(data):
    """Converts a reStructuredText into its node
    """
    if not data:
        return
    parser = docutils.parsers.rst.Parser()
    document = docutils.utils.new_document('<>')
    document.settings = docutils.frontend.OptionParser().get_default_values()
    document.settings.tab_width = 4
    document.settings.pep_references = False
    document.settings.rfc_references = False
    document.settings.env = Env()
    parser.parse(data, document)
    if len(document.children) == 1:
        return document.children[0]
    else:
        par = docutils.nodes.paragraph()
        for child in document.children:
            par += child
        return par

def setup(app):
    """
    """
    app.add_config_value('janitoo_source', False, 'html')
    app.add_directive('jnt-extensions', ExtensionDirective)

