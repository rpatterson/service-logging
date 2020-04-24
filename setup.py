"""
Python logging configurations done The Right Way, distribution/package metadata.
"""

import setuptools

with open("README.rst", "r") as readme:
    LONG_DESCRIPTION = readme.read()

tests_require = ['contextlib2;python_version<"3"', 'pathlib2;python_version<"3"']

setuptools.setup(
    name="service-logging",
    author="Ross Patterson",
    author_email="me@rpatterson.net",
    description=(
        "Python logging configurations done The Right Way "
        "for programs that may run in the foreground or background"
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    url="https://github.com/rpatterson/service-logging",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
    ],
    keywords="logging syslog nteventlog console",
    python_requires=">=2.7",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    use_scm_version=dict(
        write_to="src/servicelogging/version.py", local_scheme="no-local-version",
    ),
    setup_requires=["setuptools_scm"],
    install_requires=["six"],
    tests_require=tests_require,
    extras_require=dict(
        dev=tests_require
        + [
            "pytest",
            "pre-commit",
            "coverage",
            "flake8",
            "autoflake",
            "autopep8",
            'flake8-black;python_version>="3"',
        ],
        loguru=['loguru;python_version>="3"'],
    ),
    entry_points=dict(console_scripts=["service-logging=servicelogging:main"]),
)
