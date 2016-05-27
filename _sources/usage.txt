=====
Usage
=====

Janitoo provides helpers for writing documentation with sphinx.
All informations are extracted from setup.py.

jnt-package
===========

You can add the package name, description and long_description of a package adding :

.. code:: bash

    .. jnt-package::
        :infos: name,desc,long_desc

Look at reference document for all availlable options.

jnt-extensions
==============

You can add the extensions in package using :

.. code:: bash

    .. jnt-extensions::
        :entry: entry name of the extension. If not set, all extensions are injected.
        :types: types of extension. If not set, all types are injected.

Look at reference document for all availlable options.

jnt-badges
==========

You can add the package bagdes :

.. code:: bash

    .. jnt-badge::
        :badges: travis, ...

Look at reference document for all availlable options.
