"""
Demo or testing script that just logs messages in the background.
"""

import sys
import os
import subprocess

dirname = os.path.dirname(__file__)

popen = subprocess.Popen(
    [
        sys.executable,
        os.path.join(dirname, "servicelogging.py"),
        os.path.join(dirname, "foreground_demo.py"),
    ],
    stderr=subprocess.PIPE,
)
print(popen.communicate()[1])
