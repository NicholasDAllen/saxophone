from setuptools import setup
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/saxophone/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name="saxophone",
    version=version,
    url="https://github.com/nicholasdallen/saxophone",
    author="Nicholas Allen",
    author_email="nick@nicholasdallen.com",
    description='A user-friendly xml query interface for python'
                'that is built on SAX for speed',
    packages=["saxophone"],
    package_dir={"": "src"},
    install_requires=[
        'six'
    ]
)
