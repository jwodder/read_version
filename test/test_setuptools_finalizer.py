from   os.path    import dirname, join
from   subprocess import CalledProcessError, STDOUT, check_output
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
    ('flat-path', '--version', '23.42'),
    ('slash-path', '--version', '1.2.3.4'),
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
def test_setuptools_finalizer_with_toml_nopath():
    with pytest.raises(CalledProcessError) as excinfo:
        check_output(
            ['python', 'setup.py', '--version'],
            cwd=join(PROJECT_DIR, 'nopath'),
            stderr=STDOUT,
        )
    r = excinfo.value.output
    if not isinstance(r, str):
        # Python 3
        r = r.decode()
    assert '"path" key of tool.read_version.version not set in pyproject.toml' \
        in r

@pytest.mark.skipif(not has_toml, reason='Requires toml package')
def test_setuptools_finalizer_with_toml_missing_variable():
    with pytest.raises(CalledProcessError) as excinfo:
        check_output(
            ['python', 'setup.py', '--version'],
            cwd=join(PROJECT_DIR, 'missing'),
            stderr=STDOUT,
        )
    r = excinfo.value.output
    if not isinstance(r, str):
        # Python 3
        r = r.decode()
    assert "No assignment to '__version__' found in file" in r

@pytest.mark.skipif(has_toml, reason='Requires toml package not installed')
@pytest.mark.parametrize('project,option,value', [
    ('flat-path', '--version', '0.0.0'),
    ('slash-path', '--version', '0.0.0'),
    ('list-path', '--version', '0.0.0'),
    ('altvariable', '--version', '0.0.0'),
    ('missing', '--version', '0.0.0'),
    ('missing-default', '--version', '0.0.0'),
    ('present-default', '--version', '0.0.0'),
    ('nopath', '--version', '0.0.0'),
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
