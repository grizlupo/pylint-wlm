from setuptools import setup, find_packages


setup(
    name = 'pylint-wlm',
    version = '0.0.1',
    url = '',
    author = 'LSY',
    author_email = 'grizlupo@daum.net',
    description = 'pylint plugin for wlm',
    install_requires = ['astroid'],
    packages = find_packages(exclude=['docs', 'tests*']),
    python_requires = '>=3.6',
    license = 'MIT'
)
