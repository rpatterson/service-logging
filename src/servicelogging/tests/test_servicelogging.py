"""
service-logging unit and integration tests.
"""

import logging
import unittest

# BBB: Python 2 compatibility
try:
    import contextlib2 as contextlib
except ImportError:  # pragma: no cover
    import contextlib
try:
    import pathlib
except ImportError:  # pragma: no cover
    import pathlib2 as pathlib

import six

import servicelogging

PROJECT_PATH = pathlib.Path(__file__).parents[3]


class ServiceLoggingTests(unittest.TestCase):
    """
    service-logging unit and integration tests.
    """

    EXAMPLE_SCRIPT_PATH = PROJECT_PATH / "background_demo.py"

    def getCliErrorMessages(self, args):
        """
        Run the CLI script and return any error messages.
        """
        stderr_file = six.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(stderr_file):
                servicelogging.main(args=args)
        return stderr_file.getvalue()

    def test_cli_help(self):
        """
        The command line script is self-docummenting.
        """
        stdout_file = six.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(stdout_file):
                servicelogging.main(args=["--help"])
        stdout = stdout_file.getvalue()
        self.assertIn(
            servicelogging.__doc__.strip(),
            stdout,
            "The console script name missing from --help output",
        )

    def test_cli_options(self):
        """
        The command line script accepts options controlling behavior.
        """
        result = servicelogging.main(args=[str(self.EXAMPLE_SCRIPT_PATH)])
        self.assertIsNone(
            result, "Wrong console script options return value",
        )

    def test_cli_option_errors(self):
        """
        The command line script displays useful messages for invalid option values.
        """
        stderr = self.getCliErrorMessages(
            args=["--level=DEBUG", "__non_existent_file__"]
        )
        self.assertIn(
            "Could not resolve '__non_existent_file__'",
            stderr,
            "Wrong invalid script argument message",
        )

        stderr = self.getCliErrorMessages(
            args=["--level=getLogger", str(self.EXAMPLE_SCRIPT_PATH)]
        )
        self.assertIn(
            "doesn't correspond to a logging level",
            stderr,
            "Wrong invalid --level option message",
        )

        stderr = self.getCliErrorMessages(
            args=[
                "--level=__non_existent_logging_module_attribute__",
                str(self.EXAMPLE_SCRIPT_PATH),
            ]
        )
        self.assertIn(
            "Could not look up logging level",
            stderr,
            "Wrong invalid --level option message",
        )

        logging.__non_level_int_attribute__ = 999
        try:
            stderr = self.getCliErrorMessages(
                args=[
                    "--level=__non_level_int_attribute__",
                    str(self.EXAMPLE_SCRIPT_PATH),
                ]
            )
        finally:
            del logging.__non_level_int_attribute__
        self.assertIn(
            "doesn't match the given level name",
            stderr,
            "Wrong non-level integer attribute --level option message",
        )
