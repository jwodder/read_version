.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://travis-ci.org/jwodder/read_version.svg?branch=master
    :target: https://travis-ci.org/jwodder/read_version

.. image:: https://codecov.io/gh/jwodder/read_version/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/read_version

.. image:: https://img.shields.io/pypi/pyversions/read_version.svg
    :target: https://pypi.org/project/read_version/

.. image:: https://img.shields.io/github/license/jwodder/read_version.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/read_version>`_
| `PyPI <https://pypi.org/project/read_version/>`_
| `Issues <https://github.com/jwodder/read_version/issues>`_

When creating a ``setup.py`` for a new project, do you find yourself always
writing the same block of code for parsing ``__version__`` from your project's
source?  Something like this?

::

    with open(join(dirname(__file__), 'package_name', '__init__.py')) as fp:
        for line in fp:
            m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
            if m:
                version = m.group(2)
                break
        else:
            raise RuntimeError('Unable to find own __version__ string')

    setup(
        version = version,
        ...
    )

Someone needs to put all that into a reusable package, am I right?  Well,
someone did, and this is that package.

Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``read_version``::

    pip install read_version


Usage
=====
1. Install ``read_version`` in your development environment.

2. Add a ``pyproject.toml`` file to your project declaring ``read_version`` as
   a build dependency.  (This is needed so that other people can build your
   package from source; see `PEP 518
   <https://www.python.org/dev/peps/pep-0518/>`_ for more information.)  The
   contents of the file should look like::

        [build-system]
        requires = [
            "read_version",
            "setuptools",
            "wheel"
        ]

3. In your ``setup.py``, get rid of your boilerplate ``__version__``-finding
   code and replace it with::

        from read_version import read_version

        version = read_version('packagename', '__init__.py')

        setup(
            version = version,
            ...
        )

4. Done!


API
===
``read_version`` exports a single function, also named ``read_version``, whose
signature is::

    read_version(*filepath, variable='__version__', default=NOTHING)

``read_version()`` requires one or more file path components as positional
arguments specifying what file to parse ``__version__`` from.  The path
components will be joined together with ``os.path.join()``, and then, if the
path isn't absolute, the directory containing the script calling
``read_version()`` will be prepended to the path.  (No more
``join(dirname(__file__), ...)`` boilerplate needed!)

By default, ``read_version()`` searches for assignments to a variable named
``__version__``, returning the value of the last assignment.  A different
variable name can be searched for instead by setting the ``variable`` keyword
argument to the name of the desired variable.

If no assignments to the variable are found, a ``ValueError`` is raised.  To
instead return a default value, set the ``default`` keyword argument.


Restrictions
============
``read_variable`` only finds assignments to ``__version__`` that occur at the
top level of the module, outside of any blocks.

Only assignments of literal values to ``__version__`` are supported; more
complicated expressions will cause an error to be raised.
