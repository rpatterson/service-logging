"""
Python logging configurations done The Right Way.
"""

import sys
import os
import logging
from logging import handlers
import argparse

import mainwrapper

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

try:
    import loguru
except ImportError:  # pragma: no cover
    loguru = None


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

MESSAGE_FMT = "%(name)s %(levelname)s %(message)s"
message_formatter = logging.Formatter(MESSAGE_FMT)


def setup_fmts():
    """
    Set the global format strings.

    Need a function because cannot be set at import time if running as a
    wrapper for another script.
    """
    global APPNAME
    global SYSLOG_PREFIX
    global SYSLOG_FMT
    global syslog_formatter

    APPNAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    SYSLOG_PREFIX = "{0}[%(process)d]: ".format(APPNAME)
    SYSLOG_FMT = SYSLOG_PREFIX + MESSAGE_FMT
    syslog_formatter = logging.Formatter(SYSLOG_FMT)


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


class SysLogHandler(handlers.SysLogHandler):
    """
    Also map common custom logging levels, such as VERBOSE.
    """

    priority_map = dict(
        handlers.SysLogHandler.priority_map,
        **{"TRACE": "debug", "VERBOSE": "debug", "SUCCESS": "notice"}
    )


def choose_handler(**kwargs):  # pragma: no cover
    """
    Choose the best handler for the current OS and context.

    `kwargs` are passed onto the handler class instantiation after
    supplementing based on the current OS and context.
    """
    if sys.stderr.isatty():
        handler = logging.StreamHandler(**kwargs)
        handler.setFormatter(message_formatter)
    elif sys.platform == "win32":
        if win32evtlog is None:
            raise ValueError(
                "The Python Win32 extensions are not available.  "
                "Please install the `pywin32` distribution."
            )
        kwargs.setdefault("appname", APPNAME)
        handler = handlers.NTEventLogHandler(**kwargs)
        handler.setFormatter(syslog_formatter)
    else:
        if SYSLOG_SOCKET:
            kwargs.setdefault("address", SYSLOG_SOCKET)
        handler = SysLogHandler(**kwargs)
        handler.setFormatter(syslog_formatter)

    return handler


def basicConfig(level=logging.INFO):
    """
    Choose the handler and install it in the root handler.

    Also choose the appropriate LEVEL.
    """
    if loguru is not None:  # pragma: no cover
        add_loguru_level_names()

    root = logging.getLogger()
    if not root.handlers:  # pragma: no cover
        handler = choose_handler()
        root.addHandler(handler)
        root.setLevel(level)


if loguru is not None:  # pragma: no cover

    def add_loguru_level_names(
        loguru_levels=loguru.logger._core.levels, levels_by_name=logging._nameToLevel
    ):
        """
        Add custom loguru level names to prevent ambiguous `Level ##` in messages.
        """
        for loguru_level_name, loguru_level in loguru_levels.items():
            for level_name in (loguru_level_name, loguru_level.name):
                if level_name not in levels_by_name:
                    logging.addLevelName(loguru_level.no, level_name)


@mainwrapper.wrap_main(parser)
def main(level=parser.get_default("level")):
    """
    Run the Python script provided with logging configured.
    """
    setup_fmts()
    basicConfig(level=level)


main.__doc__ = __doc__
