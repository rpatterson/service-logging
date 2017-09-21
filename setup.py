"""
Python logging configurations done The Right Way
"""

import os

from setuptools import setup, find_packages

version = '0.1'

setup(
    name='service-logging',
    version=version,
    description=(
        'Python logging configurations done The Right Way '
        'for programs that may run in the foreground or background'),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
    ],
    keywords='logging syslog nteventlog console',
    author='Ross Patterson',
    author_email='me@rpatterson.net',
    url='https://pypi.python.org/pypi/service-logging',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'six',
      ],
    entry_points=dict(console_scripts=['servicelogging=servicelogging:main']),
)
