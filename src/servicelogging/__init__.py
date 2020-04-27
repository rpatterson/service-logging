"""
Python logging configurations done The Right Way.
"""

import sys
import os
import logging
from logging import handlers
import argparse

import six

# Manage version through the VCS CI/CD process
try:
    from . import version
except ImportError:  # pragma: no cover
    version = None
if version is not None:  # pragma: no cover
    __version__ = version.version

try:
    import win32evtlog
except ImportError:
    win32evtlog = None


def logging_level_type(level_name):
    """
    Lookup the logging level corresponding to the named level.
    """
    try:
        level = getattr(logging, level_name)
    except Exception as exc:
        raise argparse.ArgumentTypeError(
            "Could not look up logging level from name:\n{}".format(exc.args[0])
        )
    if not isinstance(level, int):
        raise argparse.ArgumentTypeError(
            "Level name {!r} doesn't correspond to a logging level, got {!r}".format(
                level_name, level
            )
        )

    looked_up_level_name = logging.getLevelName(level)
    if looked_up_level_name != level_name:
        raise argparse.ArgumentTypeError(
            (
                "Looked up logging level {!r} "
                "doesn't match the given level name {!r}"
            ).format(level, level_name)
        )

    return level


# Define command line options and arguments
parser = argparse.ArgumentParser(
    description=__doc__.strip(), formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--level",
    default=logging.INFO,
    type=logging_level_type,
    help="The level of messages to log at or above",
)
parser.add_argument(
    "script",
    type=argparse.FileType("r"),
    help="The Python script to run after configuring logging",
)

MESSAGE_FMT = "%(name)s %(levelname)s %(message)s"


def setup_fmts():
    """
    Set the global format strings.

    Need a function because cannot be set at import time if running as a
    wrapper for another script.
    """
    global APPNAME
    global SYSLOG_PREFIX
    global SYSLOG_FMT

    APPNAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    SYSLOG_PREFIX = "{0}[%(process)d]: ".format(APPNAME)
    SYSLOG_FMT = SYSLOG_PREFIX + MESSAGE_FMT


setup_fmts()


# Import time OS-specific detection

SYSLOG_SOCKETS = (
    "/dev/log",  # Linux
    "/var/run/syslog",  # OS X
    "/var/run/logpriv",  # BSD
    "/var/run/log",  # BSD
)
SYSLOG_SOCKET = None
for socket_name in SYSLOG_SOCKETS:  # pragma: no cover
    if os.path.exists(socket_name):
        SYSLOG_SOCKET = socket_name
        break


def choose_handler(**kwargs):  # pragma: no cover
    """
    Choose the best handler for the current OS and context.

    `kwargs` are passed onto the handler class instantiation after
    supplementing based on the current OS and context.
    """
    if sys.stderr.isatty():
        handler = logging.StreamHandler(**kwargs)
        formatter = logging.Formatter(MESSAGE_FMT)
        handler.setFormatter(formatter)
    elif sys.platform == "win32":
        if win32evtlog is None:
            raise ValueError(
                "The Python Win32 extensions are not available.  "
                "Please install the `pywin32` distribution."
            )
        kwargs.setdefault("appname", APPNAME)
        handler = handlers.NTEventLogHandler(**kwargs)
        formatter = logging.Formatter(SYSLOG_FMT)
        handler.setFormatter(formatter)
    else:
        if SYSLOG_SOCKET:
            kwargs.setdefault("address", SYSLOG_SOCKET)
        handler = handlers.SysLogHandler(**kwargs)
        formatter = logging.Formatter(SYSLOG_FMT)
        handler.setFormatter(formatter)

    return handler


def basicConfig(level=logging.INFO):
    """
    Choose the handler and install it in the root handler.

    Also choose the appropriate LEVEL.
    """
    root = logging.getLogger()
    if not root.handlers:  # pragma: no cover
        handler = choose_handler()
        root.addHandler(handler)
        root.setLevel(level)


def main(args=None):
    """
    Run the Python script provided with logging configured.
    """
    import __main__

    args, remaining = parser.parse_known_args(args)
    sys.argv[0] = args.script.name
    sys.argv[1:] = remaining
    # Insert the script's dir in front of module search path.
    sys.path.insert(0, os.path.dirname(args.script.name))
    setup_fmts()

    basicConfig(level=args.level)

    exec_ = six.exec_
    __builtins__ = __main__.__dict__["__builtins__"]
    __main__.__dict__.clear()
    __main__.__dict__.update(
        __name__="__main__",
        __file__=args.script.name,
        __package__=None,
        __cached__=None,
        __builtins__=__builtins__,
    )

    return exec_(compile(args.script.read(), args.script.name, "exec"))


main.__doc__ = __doc__


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
