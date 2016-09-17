================================================
service-logging
================================================
Python logging configurations done The Right Way
------------------------------------------------

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

Use ``servicelogging.basicConfig()`` to ad an OS and context specific root
logging hander::

    >>> import servicelogging
    >>> servicelogging.basicConfig()

You can also use ``servicelogging`` as a script to run another script with
logging configured::

    $ python -m servicelogging foreground_demo.py
    $ python servicelogging.py background_demo.py
    $ servicelogging foreground_demo.py

Or if you just want the appropriate handler to use as you'd like in your code,
you can use ``servicelogging.choose_handler()``::

    >>> import servicelogging
    >>> handler = servicelogging.choose_handler()
