==============================================================================
service-logging
==============================================================================
Python logging configurations done The Right Way
------------------------------------------------------------------------------

.. image:: https://github.com/rpatterson/service-logging/workflows/Run%20linter,%20tests%20and,%20and%20release/badge.svg

Using logging correctly is often both context and OS specific.  For a context
specific example, when developing a daemon or service it is often useful to
use one logging configuration when running in the foreground in a shell and
another when running in the background as a daemon.  For an OS specific
example, when running in the background a service should use the appropriate
logging service for that system so that logging metadata is correct (severity,
facility, etc.), but the right way to do that is OS specific.  Furthermore,
the deciding between these configurations requires programatic logic and
cannot be done through the simple configuration mechanisms provided by the
Python ``logging`` package.

Given these realities, logging is often not done "The Right Way" and/or
difficult to adjust for debugging/testing vs background.  ``service-logging``
aims to address this by providing both correct logging configurations for
different contexts/OSes and providing the logic to choose between them.  It
also provides various ways to use these configurations making the depth of
commitment opt-in.


Installation
============

Install using any tool for installing standard Python 3 distributions such as `pip`_::

  $ sudo pip3 install service-logging


Usage
=====

Use ``servicelogging.basicConfig()`` to ad an OS and context specific root
logging hander::

  >>> import servicelogging
  >>> servicelogging.basicConfig()

The command-line script also supports wrapping another Python script with logging
configured::

  $ python -m servicelogging foreground_demo.py
  $ python servicelogging.py background_demo.py
  $ service-logging foreground_demo.py

See the command-ling help for details on options and arguments::

  $ service-logging --help
  usage: service-logging [-h] [--level LEVEL] script

  python logging configurations done The Right Way, top-level package.

  positional arguments:
    script         The Python script to run after configuring logging

  optional arguments:
    -h, --help     show this help message and exit
    --level LEVEL  The level of messages to log at or above (default: 20)

Or if you just want the appropriate handler to use as you'd like in your code,
you can use ``servicelogging.choose_handler()``::

  >>> import servicelogging
  >>> handler = servicelogging.choose_handler()


.. _pip: https://pip.pypa.io/en/stable/installing/
