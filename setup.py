from setuptools import setup, find_packages

version = '0.1'

setup(
    name='service-logging',
    version=version,
    description=(
        'Python logging configurations done The Right Way '
        'for programs that may run in the foreground or background'),
    long_description='',
    classifiers=[],
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
      ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
