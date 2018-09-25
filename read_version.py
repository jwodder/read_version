"""
Extract your project's __version__ variable

Visit <https://github.com/jwodder/read_version> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'read-version@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/read_version'

import ast
import inspect
import os.path

__all__ = ['read_version']

def read_version(*fpath, variable='__version__', **kwargs):
    if not fpath:
        raise ValueError('No filepath passed to read_version()')
    fpath = os.path.join(fpath)
    if not os.path.isabs(fpath):
        caller_file = inspect.stack()[1][0].f_globals["__file__"]
        fpath = os.path.join(os.path.dirname(caller_file), fpath)
    with open(fpath, 'rb') as fp:
        src = fp.read()
    top_level = ast.parse(src)
    try:
        result = kwargs["default"]
    except KeyError:
        pass
    for statement in top_level.body:
        if isinstance(statement, ast.Assign):
            try:
                value = ast.literal_eval(statement.value)
            except (TypeError, ValueError):
                pass
            else:
                for target in statement.targets:
                    if isinstance(target, ast.Tuple):
                        for t,v in zip(target.elts, value):
                            assert isinstance(t, ast.Name)
                            if t.id == variable:
                                result = v
                    elif target.id == variable
                        result = value
    try:
        return result
    except NameError:
        raise ValueError('No assignment to {!r} found in file'.format(variable))
