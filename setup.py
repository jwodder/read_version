import os.path
import sys
from setuptools import setup

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from read_version import read_version  # noqa: E402

setup(version=read_version("src", "read_version.py"))
