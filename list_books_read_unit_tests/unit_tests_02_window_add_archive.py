# -*- coding: utf-8 -*- noqa
"""
Created on Sun Dec 22 10:22:48 2024

@author: JTS
"""
import logging
import os
import sys
import unittest

from datetime import datetime, timezone

from list_books_read_code import Database
from list_books_read_code import WindowAddArchive

UNIT_TESTS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIRECTORY = os.path.dirname(UNIT_TESTS_DIRECTORY)

LOGGING_DIRECTORY = os.path.join(
    PROJECT_DIRECTORY,
    'unit_tests_logs',
    'window_add_archive_only',
)


class TestWindowAddArchive(unittest.TestCase):
    """Unit test of Database class."""

    def setUp(self):
        """
        Set up class before each test.

        Returns
        -------
        None.

        """
        logging.info('Set up test.')

        self.database_name = 'test.db'
        self.languages_file = './test_data/languages.data'
        self.statuses_file = "./test_data/statuses.data"

        if os.path.exists(self.database_name):
            os.remove(self.database_name)

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

    def tearDown(self):
        """
        Tear down class after each test.

        Returns
        -------
        None.

        """
        logging.info('Tear down test.')

        if hasattr(self, 'window_add_archive'):
            del self.window_add_archive

        if hasattr(self, 'database'):
            del self.database

        if os.path.exists(self.database_name):
            os.remove(self.database_name)

        del self.database_name
        del self.languages_file
        del self.statuses_file

    def test_01_window_pops_up_correctly_until_closed(self):
        """
        Test if the window pops up correctly and stays until closed by user.

        Returns
        -------
        None.

        """
        self.window_add_archive = WindowAddArchive(
            self.database)
        self.window_add_archive.render()
        still_open = True
        while still_open:
            still_open = self.window_add_archive.update()


if __name__ == '__main__':
    os.chdir(PROJECT_DIRECTORY)

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

    tests = unittest.TestLoader().loadTestsFromModule(
        __import__('__main__'),
        pattern='Test*',
    )
    results = unittest.TextTestRunner(verbosity=1).run(tests)

    logging.shutdown()

    sys.exit()
