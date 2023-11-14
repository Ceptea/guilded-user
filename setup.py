'''
setup
'''
from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Api wrapper for guilded user api "

setup(
    name="guilded_user",
    version=VERSION,
    author="Ceptea",
    author_email="c-e-pt-e-@outlook.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["guilded_user", "guilded user api"],
)
