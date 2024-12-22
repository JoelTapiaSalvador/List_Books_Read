# -*- coding: utf-8 -*- noqa
"""
Created on Wed Nov 13 20:03:25 2024

@author: JTS
"""
import logging
import os
import unittest

from datetime import datetime, timezone

CODE_DIRECTORY = os.path.join(
    '..',
)

LOGGING_DIRECTORY = os.path.join(
    '.',
    'unit_tests_logs',
    'all_tests',
)

original_directory = os.getcwd()

os.chdir(CODE_DIRECTORY)

if __name__ == "__main__":
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
        original_directory,
        pattern='unit_tests_*.py'
    )
    results = unittest.TextTestRunner(verbosity=1).run(tests)

    logging.shutdown()

os.chdir(original_directory)
