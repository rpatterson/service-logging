"""
Demo or testing script that just logs a message for each level.
"""

import logging

logger = logging.getLogger(__name__)

for level in sorted(
        level for level in logging._levelNames
        if isinstance(level, int)):
    logger.log(level, 'Log %s level message', logging.getLevelName(level))
