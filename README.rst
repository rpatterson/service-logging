================================================
service-logging
================================================
Python logging configurations done The Right Way
------------------------------------------------

TL;DR:

  ``logging.basicConfig()`` is very often not enough, leading to DRY
  violations.  Use ``service-logging`` to log to syslog or the Windows event
  log when running in the background, and log to stderr when running in the
  foreground, both with well formatted messages.

Using logging correctly is often both usage and OS specific.  For a usage
specific example, when developing or troubleshooting a daemon and/or service
it is often useful to use one logging configuration when running in the
foreground in a shell and another when running in the background.  For an OS
specific example, when running in the background a daemon and/or service
should use the appropriate logging service for that system so that logging
metadata is correct (severity, facility, etc.), but the right way to do that
is OS specific.  Furthermore, deciding between these configurations requires
logic that cannot be done through the simple configuration mechanisms provided
by Python's ``logging.config``.

Given these realities, logging is often not done "The Right Way", and/or is
difficult to adjust for debugging/testing vs background.  ``service-logging``
aims to address this by providing the logic to choose between correct logging
configurations for different usages and OSes.  It also provides several ways
to use these configurations, making the depth of commitment opt-in.

Use ``servicelogging.basicConfig()`` to add an OS and usage specific root
logging hander::

    >>> import servicelogging
    >>> servicelogging.basicConfig()

You can also use ``servicelogging`` as a script to run another script with
logging configured::

    $ python -m servicelogging foreground_demo.py
    $ python servicelogging.py background_demo.py
    $ servicelogging foreground_demo.py

Or if you just want the appropriate handler and formatter to use as you'd like
in your code, you can use ``servicelogging.choose_handler()``::

    >>> import servicelogging
    >>> handler = servicelogging.choose_handler()


----------------------------
TODO
----------------------------
Features for future releases
____________________________

Support alternate logging configuration options:

  Make sure that the approach is compatible with the various Python
  ``logging.config`` options.

Anything else you find youself doing over and over:

  Submit a PR and make an argument for why a change would be useful in the
  vast majority of cases.
