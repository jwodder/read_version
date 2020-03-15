.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.org/jwodder/read_version.svg?branch=master
    :target: https://travis-ci.org/jwodder/read_version

.. image:: https://codecov.io/gh/jwodder/read_version/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/read_version

.. image:: https://img.shields.io/pypi/pyversions/read_version.svg
    :target: https://pypi.org/project/read_version/

.. image:: https://img.shields.io/github/license/jwodder/read_version.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/read_version>`_
| `PyPI <https://pypi.org/project/read_version/>`_
| `Issues <https://github.com/jwodder/read_version/issues>`_
| `Changelog <https://github.com/jwodder/read_version/blob/master/CHANGELOG.md>`_

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
someone did, and this is that package.  It exports a single function that does
the above, perfect for importing into your ``setup.py``, and *(New in v0.2.0!)*
this package even lets you map Python variables to supported metadata fields
via your ``pyproject.toml``.

Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``read_version``::

    pip install read_version

``read_version`` also has a ``toml`` extra that provides support for
reading configuration from ``pyproject.toml``.  Install it with::

    pip install 'read_version[toml]'


Usage
=====

The Functional Way
------------------

1. Install ``read_version`` in your development environment.

2. Add a ``pyproject.toml`` file to your project declaring ``read_version`` as
   a build dependency.  (This is needed so that other people can build your
   package from source; see `PEP 518
   <https://www.python.org/dev/peps/pep-0518/>`_ for more information.)  The
   contents of the file should look like::

        [build-system]
        requires = [
            "read_version ~= 0.2.0",
            "setuptools",
            "wheel"
        ]
        build-backend = "setuptools.build_meta"

3. In your ``setup.py``, get rid of your boilerplate ``__version__``-finding
   code and replace it with::

        from read_version import read_version

        setup(
            version = read_version('packagename', '__init__.py'),
            ...
        )

4. Done!

The Declarative Way
-------------------

*New in version 0.2.0!*

1. Install ``read_version`` in your development environment with the ``toml``
   extra::

    pip install 'read_version[toml]'

   You will also need version 42.0.0 or later of ``setuptools``::

    pip install -U 'setuptools>=42'

2. Add a ``pyproject.toml`` file to your project declaring
   ``read_version[toml]`` as a build dependency and also requiring version
   42.0.0 or later of ``setuptools``.  The relevant section of the file should
   look like::

        [build-system]
        requires = [
            "read_version[toml] ~= 0.2.0",
            "setuptools >= 42.0.0",
            "wheel"
        ]
        build-backend = "setuptools.build_meta"

3. Get rid of your boilerplate ``__version__``-finding code in your
   ``setup.py``.  Instead, add a ``tool.read_version`` table to your
   ``pyproject.toml`` file, and for each metadata field that you want to be
   read from a variable in a Python source file, add an entry to this table of
   the form ``FIELD = "dotted.file.path:varname"``, where:

   - ``FIELD`` is replaced by the lowercase name of the field.  Supported
     fields are:

     - ``author``
     - ``author_email``
     - ``description`` (Note that this is the short description or summary, not
       the long description!)
     - ``keywords`` (It is recommended to use a list of strings as the value or
       else ``setuptools`` might mangle it)
     - ``license``
     - ``maintainer``
     - ``maintainer_email``
     - ``url``
     - ``version``

     Entries with unsupported or unknown field names are ignored.

   - ``dotted.file.path`` is replaced by the path (relative to the project
     root) to the file containing the variable, with path components separated
     by dots and the ``.py`` at the end of the last path component dropped

   - ``varname`` is replaced by the name of the variable to read

   Examples::

        [tool.read_version]

        # Set the project's version to the value of __version__ in foobar.py:
        version = "foobar:__version__"

        # Set the project's author to the value of author_name in
        # foobar/__init__.py
        author = "foobar.__init__:author_name"

        # Set the project's license to the value of LICENSE in
        # src/foobar/about.py:
        license = "src.foobar.about:LICENSE"

   If this syntax doesn't work for you — say, because one of your path
   components contains a period or colon in its name, or because the file
   doesn't have a ``.py`` extension — or if you want to set a default value for
   when the variable isn't found, use a table value for the field instead of a
   string, like so::

        [tool.read_version]

        # Set the project's version to the value of __version__ in
        # foo.bar/__init__.pyq:
        version = { path = ["foo.bar", "__init__.pyq"], variable = "__version__" }

        # Set the project's author_email to the value of EMAIL in foobar.py.
        # If the variable isn't found, use the value "me@example.com" instead
        # of erroring
        author_email = { path = ["foobar.py"], variable = "EMAIL", default = "me@example.com" }


   Table values may contain the following keys:

   :path: *(Required)* The path to the source file containing the variable to
          read, relative to the project root; this may be given as either a
          forward-slash-separated path or as a list of path components
   :variable: *(Required)* The name of the Python variable to get the value
              from
   :default: *(Optional)* If the variable cannot be found in the source file,
             use the given value instead; if the variable cannot be found and
             ``default`` is not set, an error will occur

4. Done!

API
===
``read_version`` exports a single function, also named ``read_version``, whose
signature is::

    read_version(*filepath, variable='__version__', default=NOTHING)

``read_version()`` takes one or more file path components pointing to a Python
source file to parse.  The path components will be joined together with
``os.path.join()``, and then, if the path isn't absolute, the path to the
directory containing the script calling ``read_version()`` will be prepended to
the path.  (No more ``join(dirname(__file__), ...)`` boilerplate needed!)
``read_version()`` then parses the given Python file and searches through the
parse tree for any assignments to a variable named ``__version__``, returning
the last value assigned.

The ``variable`` keyword argument can be set to the name of a variable other
than ``__version__`` to search for assignments to a different variable instead.

If no assignments to the variable are found, a ``ValueError`` is raised.  To
instead return a default value when this happens, set the ``default`` keyword
argument.


Restrictions
============
``read_variable`` only finds assignments that occur at the top level of the
module, outside of any blocks.

Only assignments of literal values are supported; assignments to the
searched-for variable involving more complicated expressions will cause an
error to be raised.
