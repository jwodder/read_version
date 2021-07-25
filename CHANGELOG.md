v0.3.2 (2021-07-25)
-------------------
- Support Python 3.9
- Drop support for Python 2.7 and 3.5
- Declare the project inactive and no longer supported

v0.3.1 (2020-07-12)
-------------------
- Import setuptools before importing distutils.  This way, users who import
  `read_version` before importing setuptools 49.2.0 (or any later versions with
  the same behavior) will not get a warning about importing distutils before
  setuptools.
- Add setuptools as a dependency

v0.3.0 (2020-03-17)
-------------------
- Support fetching module docstrings with `variable="__doc__"`

v0.2.0 (2020-03-16)
-------------------
- Support Python 3.8
- Drop support for Python 3.4
- Support describing what attributes to read from where via a `pyproject.toml`
  file

v0.1.1 (2019-04-27)
-------------------
- Fix an inability to cope with assignments to subscripts etc.

v0.1.0 (2018-09-25)
-------------------
Initial release
