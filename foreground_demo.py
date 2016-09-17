"""
Demo or testing script that just logs a message for each level.
"""

import sys
import os
import logging

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

for level in sorted(
        level for level in logging._levelNames
        if isinstance(level, int)):
    logger.log(level, 'Log %s level message', logging.getLevelName(level))
