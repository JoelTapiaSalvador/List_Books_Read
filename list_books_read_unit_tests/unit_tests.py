# -*- coding: utf-8 -*- noqa
"""
Created on Wed Nov 13 20:03:25 2024

@author: JTS
"""
import logging
import os
import sys
import unittest

from datetime import datetime, timezone

UNIT_TESTS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIRECTORY = os.path.dirname(UNIT_TESTS_DIRECTORY)

LOGGING_DIRECTORY = os.path.join(
    PROJECT_DIRECTORY,
    'unit_tests_logs',
    'all_tests',
)

if __name__ == "__main__":
    os.chdir(UNIT_TESTS_DIRECTORY)

    os.makedirs(LOGGING_DIRECTORY, exist_ok=True)

    logging_file_name = datetime.now(timezone.utc).strftime(
        '%Y-%m-%d--%H-%M--%Z.log'
    )

    logging_path = os.path.join(LOGGING_DIRECTORY, logging_file_name)

    logging

    logging.basicConfig(
        filename=logging_path,
        filemode='w',
        level=logging.DEBUG,
        force=True,
        format='[%(asctime)s] %(levelname)s:\n\tModule: "%(module)s"\n\t' +
        'Function: "%(funcName)s"\n\tLine: %(lineno)d\n\t\t%(message)s\n',
    )

    tests = unittest.TestLoader().discover(
        UNIT_TESTS_DIRECTORY,
        pattern='unit_tests_*.py',
        top_level_dir=PROJECT_DIRECTORY,
    )

    os.chdir(PROJECT_DIRECTORY)

    results = unittest.TextTestRunner(verbosity=1).run(tests)

    logging.shutdown()

    sys.exit()
