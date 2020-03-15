r"""
Extract your project's __version__ variable

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

Visit <https://github.com/jwodder/read_version> for more information.
"""

__version__      = '0.2.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'read-version@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/read_version'

import ast
from   distutils import log
from   errno     import ENOENT
import inspect
import os
import os.path
import sys

__all__ = ['read_version']

def read_version(*fpath, **kwargs):
    """
    ``read_version()`` takes one or more file path components pointing to a
    Python source file to parse.  The path components will be joined together
    with ``os.path.join()``, and then, if the path isn't absolute, the path to
    the directory containing the script calling ``read_version()`` will be
    prepended to the path.  (No more ``join(dirname(__file__), ...)``
    boilerplate needed!)  ``read_version()`` then parses the given Python file
    and searches through the parse tree for any assignments to a variable named
    ``__version__``, returning the last value assigned.

    The ``variable`` keyword argument can be set to the name of a variable
    other than ``__version__`` to search for assignments to a different
    variable instead.

    If no assignments to the variable are found, a ``ValueError`` is raised.
    To instead return a default value when this happens, set the ``default``
    keyword argument.
    """

    if not fpath:
        raise ValueError('No filepath passed to read_version()')
    fpath = os.path.join(*fpath)
    if not os.path.isabs(fpath):
        caller_file = inspect.stack()[1][0].f_globals["__file__"]
        fpath = os.path.join(os.path.dirname(caller_file), fpath)
    with open(fpath, 'rb') as fp:
        src = fp.read()
    top_level = ast.parse(src)
    variable = kwargs.get("variable", "__version__")
    try:
        result = kwargs["default"]
    except KeyError:
        pass
    for statement in top_level.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Tuple):
                    if any(isinstance(t, ast.Name) and t.id == variable
                           for t in target.elts):
                        value = ast.literal_eval(statement.value)
                        for t,v in zip(target.elts, value):
                            if isinstance(t, ast.Name) and t.id == variable:
                                result = v
                elif isinstance(target, ast.Name) and target.id == variable:
                    result = ast.literal_eval(statement.value)
    try:
        return result
    except NameError:
        raise ValueError('No assignment to {!r} found in file'.format(variable))


SETTABLE_METADATA_ATTRIBUTES = {
    'author',
    'author_email',
    'description',
    'keywords',
    'license',
    'maintainer',
    'maintainer_email',
    'url',
    'version',
}

try:
    basestring
except NameError:
    basestring = str

def setuptools_finalizer(dist):
    # I *think* it's reasonable to assume that the project root is always the
    # current directory when this function is called.  Setuptools doesn't seem
    # to have decent support for running `setup.py` from another directory, and
    # the pep517.build command changes the working directory to the project
    # directory when run.  PEP 517 also says, "All hooks are run with working
    # directory set to the root of the source tree".
    PROJECT_ROOT = os.path.abspath(os.curdir)
    try:
        import toml
    except ImportError:
        log.info('read_version: toml not installed; not using pyproject.toml')
        return
    try:
        cfg = toml.load(os.path.join(PROJECT_ROOT, 'pyproject.toml'))
    except IOError as e:
        if e.errno == ENOENT:
            log.info('read_version: pyproject.toml not found')
            return
        else:
            raise
    cfg = cfg.get("tool", {}).get("read_version", {})
    if not isinstance(cfg, dict):
        log.warn('read_version: "tool.read_version" is not a table; ignoring')
        return
    for attrib, spec in cfg.items():
        if attrib in SETTABLE_METADATA_ATTRIBUTES:
            if isinstance(spec, basestring):
                modpath, _, varname = spec.partition(':')
                if not modpath or not varname:
                    sys.exit('tool.read_version.{}: Invalid specifier {!r}'
                             .format(attrib, spec))
                path = modpath.split('.')
                path[-1] += '.py'
                path = os.path.join(PROJECT_ROOT, *path)
                kwargs = {"variable": varname}
            elif isinstance(spec, dict):
                try:
                    path = spec["path"]
                except KeyError:
                    sys.exit(
                        '"path" key of tool.read_version.{} missing in'
                        ' pyproject.toml'.format(attrib)
                    )
                if isinstance(path, list):
                    path = os.path.join(PROJECT_ROOT, *path)
                else:
                    path = os.path.join(PROJECT_ROOT, path)
                try:
                    varname = spec["variable"]
                except KeyError:
                    sys.exit(
                        '"variable" key of tool.read_version.{} missing in'
                        ' pyproject.toml'.format(attrib)
                    )
                kwargs = {"variable": varname}
                if 'default' in cfg[attrib]:
                    kwargs['default'] = spec['default']
            else:
                sys.exit('tool.read_version.{} must be a string or table'
                         .format(attrib))
            log.info('read_version: reading %s value from file', attrib)
            value = read_version(path, **kwargs)
            setattr(dist.metadata, attrib, value)
        else:
            log.warn('read_version: ignoring unknown field %r', attrib)
