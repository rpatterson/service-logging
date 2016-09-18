"""
Python logging configurations done The Right Way
"""

import sys
import os
import logging
from logging import handlers
import argparse

import six

try:
    import win32evtlog
except ImportError:
    win32evtlog = None

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--level', default=logging.INFO,
    help='The level of messages to log at or above')
parser.add_argument(
    'script', type=open,
    help='The Python script to run after configuring logging')

MESSAGE_FMT = '%(name)s %(levelname)s %(message)s'


# Import time OS-specific detection

SYSLOG_SOCKETS = (
    '/dev/log',  # Linux
    '/var/run/syslog',  # OS X
    '/var/run/logpriv',  # BSD
    '/var/run/log',  # BSD
    )
SYSLOG_SOCKET = None
for socket_name in SYSLOG_SOCKETS:
    if os.path.exists(socket_name):
        SYSLOG_SOCKET = socket_name
        break


def choose_handler(**kwargs):
    """
    Choose the best handler for the current OS and context.

    `kwargs` are passed onto the handler class instantiation after
    supplementing based on the current OS and context.
    """
    appname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    syslog_fmt = ('{0}[%(process)d]: ' + MESSAGE_FMT).format(appname)

    if sys.stderr.isatty():
        handler = logging.StreamHandler(**kwargs)
        formatter = logging.Formatter(MESSAGE_FMT)
        handler.setFormatter(formatter)
    elif sys.platform == 'win32':
        if win32evtlog is None:
            raise ValueError(
                'The Python Win32 extensions are not available.  '
                'Please install the `pywin32` distribution.')
        kwargs.setdefault('appname', appname)
        handler = handlers.NTEventLogHandler(**kwargs)
        formatter = logging.Formatter(syslog_fmt)
        handler.setFormatter(formatter)
    else:
        if SYSLOG_SOCKET:
            kwargs.setdefault('address', SYSLOG_SOCKET)
        handler = handlers.SysLogHandler(**kwargs)
        formatter = logging.Formatter(syslog_fmt)
        handler.setFormatter(formatter)

    return handler


def basicConfig(level=logging.INFO):
    """
    Choose the handler and install it in the root handler.

    Also choose the appropriate LEVEL.
    """
    root = logging.getLogger()
    if not root.handlers:
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
    # Replace our dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(args.script.name)

    basicConfig(level=args.level)

    exec_ = six.exec_
    __builtins__ = __main__.__dict__['__builtins__']
    __main__.__dict__.clear()
    __main__.__dict__.update(
        __name__='__main__',
        __file__=args.script.name,
        __builtins__=__builtins__)

    return exec_(compile(args.script.read(), args.script.name, 'exec'))


if __name__ == '__main__':
    sys.exit(main())
