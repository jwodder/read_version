from   os.path    import dirname, join
from   subprocess import PIPE, Popen, check_output
import pytest

try:
    import toml  # noqa
except ImportError:
    has_toml = False
else:
    has_toml = True

PROJECT_DIR = join(dirname(__file__), 'data', 'projects')

@pytest.mark.skipif(not has_toml, reason='Requires toml package')
@pytest.mark.parametrize('project,option,value', [
    ('list-path', '--version', '1.3.2.4'),
    ('altvariable', '--version', '4.2.2.3'),
    ('missing-default', '--version', '0.1.0'),
    ('present-default', '--version', '17.19'),
    ('all-attribs', '--version', '9001'),
    ('all-attribs', '--author', 'Joe Q. Author'),
    ('all-attribs', '--author-email', 'me@example.com'),
    ('all-attribs', '--description', 'Not a real package'),
    ('all-attribs', '--keywords', 'test,metadata,setuptools'),
    ('all-attribs', '--license', 'WTFPL'),
    ('all-attribs', '--maintainer', 'Manny Tainer'),
    ('all-attribs', '--maintainer-email', 'you@example.org'),
    ('all-attribs', '--url', 'https://example.net'),
    ('all-attribs-overwrite', '--version', '51a0'),
    ('all-attribs-overwrite', '--author', 'Auctor Huius'),
    ('all-attribs-overwrite', '--author-email', 'test@example.com'),
    ('all-attribs-overwrite', '--description', '*Definitely* not a real package'),
    ('all-attribs-overwrite', '--keywords',
     's,e,t,u,p,t,o,o,l,s, ,m,e,t,a,d,a,t,a, ,t,e,s,t'),
    ('all-attribs-overwrite', '--license', 'MIT'),
    ('all-attribs-overwrite', '--maintainer', 'Some gnomes'),
    ('all-attribs-overwrite', '--maintainer-email', 'gnomes@example.org'),
    ('all-attribs-overwrite', '--url', 'https://example.nil'),
    ('no-pyproject', '--version', '3.14'),
    ('epstring', '--version', '1.4.9'),
    ('epstring-dotted', '--version', '5.6.2.50'),
    ('inline-table', '--version', '3.2.2.4'),
    ('all-attribs-ep', '--version', '9001'),
    ('all-attribs-ep', '--author', 'Joe Q. Author'),
    ('all-attribs-ep', '--author-email', 'me@example.com'),
    ('all-attribs-ep', '--description', 'Not a real package'),
    ('all-attribs-ep', '--keywords', 'test,metadata,setuptools'),
    ('all-attribs-ep', '--license', 'WTFPL'),
    ('all-attribs-ep', '--maintainer', 'Manny Tainer'),
    ('all-attribs-ep', '--maintainer-email', 'you@example.org'),
    ('all-attribs-ep', '--url', 'https://example.net'),
])
def test_setuptools_finalizer_with_toml(project, option, value):
    r = check_output(
        ['python', 'setup.py', option],
        cwd=join(PROJECT_DIR, project),
    )
    if not isinstance(r, str):
        # Python 3
        r = r.decode()
    r = r.rstrip('\r\n')
    assert r == value

@pytest.mark.skipif(not has_toml, reason='Requires toml package')
@pytest.mark.parametrize('project,errmsg', [
    ('nopath', '"path" key of tool.read_version.version missing in pyproject.toml'),
    ('novariable', '"variable" key of tool.read_version.version missing in pyproject.toml'),
    # Format a unicode str so that a `u` appears at the beginning of the repr
    # in Python 2 but not Python 3
    ('missing', "No assignment to {!r} found in file".format(u'__version__')),
    ('badtype', 'tool.read_version.version must be a string or table'),
    ('str-path', '"path" key of tool.read_version.version must be a list'),
    ('badspec01', 'tool.read_version.version: Invalid specifier {!r}'.format(u'foobar:')),
    ('badspec02', 'tool.read_version.version: Invalid specifier {!r}'.format(u'foobar')),
    ('badspec03', 'tool.read_version.version: Invalid specifier {!r}'.format(u':__version__')),
])
def test_setuptools_finalizer_with_toml_error(project, errmsg):
    p = Popen(
        ['python', 'setup.py', '--version'],
        cwd=join(PROJECT_DIR, project),
        #stdout=PIPE,
        stderr=PIPE,
    )
    _, err = p.communicate()
    assert p.returncode != 0
    if not isinstance(err, str):
        # Python 3
        err = err.decode()
    assert errmsg in err

@pytest.mark.skipif(not has_toml, reason='Requires toml package')
def test_setuptools_finalizer_with_toml_not_table_warning():
    p = Popen(
        ['python', 'setup.py', '--version'],
        cwd=join(PROJECT_DIR, 'nottable'),
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    assert p.returncode == 0
    if not isinstance(out, str):
        # Python 3
        out = out.decode()
        err = err.decode()
    out = out.rstrip('\r\n')
    assert out == '0.0.0'
    assert 'read_version: "tool.read_version" is not a table; ignoring' in err

@pytest.mark.skipif(not has_toml, reason='Requires toml package')
def test_setuptools_finalizer_with_toml_unknown_field_warning():
    p = Popen(
        ['python', 'setup.py', '--version'],
        cwd=join(PROJECT_DIR, 'unkfield'),
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    assert p.returncode == 0
    if not isinstance(out, str):
        # Python 3
        out = out.decode()
        err = err.decode()
    out = out.rstrip('\r\n')
    assert out == '1.0.8'
    assert 'read_version: ignoring unknown field {!r}'.format(u'foobar') in err

@pytest.mark.skipif(has_toml, reason='Requires toml package not installed')
@pytest.mark.parametrize('project,option,value', [
    ('str-path', '--version', '0.0.0'),
    ('list-path', '--version', '0.0.0'),
    ('altvariable', '--version', '0.0.0'),
    ('missing', '--version', '0.0.0'),
    ('missing-default', '--version', '0.0.0'),
    ('present-default', '--version', '0.0.0'),
    ('nopath', '--version', '0.0.0'),
    ('novariable', '--version', '0.0.0'),
    ('all-attribs', '--version', '0.0.0'),
    ('all-attribs', '--author', 'UNKNOWN'),
    ('all-attribs', '--author-email', 'UNKNOWN'),
    ('all-attribs', '--description', 'UNKNOWN'),
    ('all-attribs', '--keywords', ''),
    ('all-attribs', '--license', 'UNKNOWN'),
    ('all-attribs', '--maintainer', 'UNKNOWN'),
    ('all-attribs', '--maintainer-email', 'UNKNOWN'),
    ('all-attribs', '--url', 'UNKNOWN'),
    ('all-attribs-overwrite', '--version', '9001'),
    ('all-attribs-overwrite', '--author', 'Joe Q. Author'),
    ('all-attribs-overwrite', '--author-email', 'me@example.com'),
    ('all-attribs-overwrite', '--description', 'Not a real package'),
    ('all-attribs-overwrite', '--keywords', 'test,metadata,setuptools'),
    ('all-attribs-overwrite', '--license', 'WTFPL'),
    ('all-attribs-overwrite', '--maintainer', 'Manny Tainer'),
    ('all-attribs-overwrite', '--maintainer-email', 'you@example.org'),
    ('all-attribs-overwrite', '--url', 'https://example.net'),
    ('no-pyproject', '--version', '3.14'),
    ('epstring', '--version', '0.0.0'),
    ('epstring-dotted', '--version', '0.0.0'),
    ('inline-table', '--version', '0.0.0'),
    ('all-attribs-ep', '--version', '0.0.0'),
    ('all-attribs-ep', '--author', 'UNKNOWN'),
    ('all-attribs-ep', '--author-email', 'UNKNOWN'),
    ('all-attribs-ep', '--description', 'UNKNOWN'),
    ('all-attribs-ep', '--keywords', ''),
    ('all-attribs-ep', '--license', 'UNKNOWN'),
    ('all-attribs-ep', '--maintainer', 'UNKNOWN'),
    ('all-attribs-ep', '--maintainer-email', 'UNKNOWN'),
    ('all-attribs-ep', '--url', 'UNKNOWN'),
    ('nottable', '--version', '0.0.0'),
    ('unkfield', '--version', '0.0.0'),
    ('badtype', '--version', '0.0.0'),
    ('badspec01', '--version', '0.0.0'),
    ('badspec02', '--version', '0.0.0'),
    ('badspec03', '--version', '0.0.0'),
])
def test_setuptools_finalizer_without_toml(project, option, value):
    r = check_output(
        ['python', 'setup.py', option],
        cwd=join(PROJECT_DIR, project),
    )
    if not isinstance(r, str):
        # Python 3
        r = r.decode()
    r = r.rstrip('\r\n')
    assert r == value
