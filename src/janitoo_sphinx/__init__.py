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

from base import JanitooDirective
from extensions import ExtensionDirective
from packages import PackageDirective

def setup(app):
    """
    """
    app.add_config_value('janitoo_source', False, 'html')
    app.add_directive('jnt-extensions', ExtensionDirective)
    app.add_directive('jnt-package', PackageDirective)

