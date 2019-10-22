try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

import os

import my_project

my_project_path = os.path.abspath(os.path.dirname(__file__))

long_description =
"""
Eine ausführliche Beschreibung des Programms.
"""

setup(
    name='my_project',
    version=my_project.__version__,
    url='http://github.com/my_account/my_project/',
    license='GPLv3',
    author='Vorname Nachname',
    author_email='name@adresse.de',
    install_requires=[
        'Flask>=0.10.1',
        'SQLAlchemy==0.8.2',
        ],
    tests_require=['nose'],
    packages=find_packages(exclude=['tests']),
    description='Eine kurze Beschreibung.',
    long_description = long_description,
    platforms='any',
    keywords = "different tags here",
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: Linux',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],

    )
