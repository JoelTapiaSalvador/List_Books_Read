# -*- coding: utf-8 -*- noqa
"""
Created on Fri Nov 15 13:47:24 2024

@author: JTS
"""
import logging
import os
import sys
import unittest

from datetime import datetime, timezone

from list_books_read_code import Database

UNIT_TESTS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIRECTORY = os.path.dirname(UNIT_TESTS_DIRECTORY)

LOGGING_DIRECTORY = os.path.join(
    PROJECT_DIRECTORY,
    'unit_tests_logs',
    'database_only',
)


class TestDatabase(unittest.TestCase):
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

    def tearDown(self):
        """
        Tear down class after each test.

        Returns
        -------
        None.

        """
        logging.info('Tear down test.')

        if hasattr(self, 'database'):
            del self.database

        if os.path.exists(self.database_name):
            os.remove(self.database_name)

        del self.database_name
        del self.languages_file
        del self.statuses_file

    def test_01_initialize_with_expected_parameters_for_first_time(self):
        """
        Test if Database class works as intended with expected parameters.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        with self.subTest(sub_test='File created.'):
            self.assertTrue(
                (
                    os.path.exists(self.database_name)
                ) and (
                    os.path.isfile(self.database_name)
                ),
                'Databse file with name does not exist.'
            )

        with self.subTest(sub_test='Read status.'):
            self.assertEqual(
                self.database.read_status,
                'Read',
                'Read status is not "Read".'
            )

        with self.subTest(sub_test='Statuses.'):
            self.assertTupleEqual(
                self.database.statuses,
                (
                    'Currently Reading',
                    'Declined',
                    'Expugned',
                    'Read',
                    'To Read',
                    'Unfinished',
                ),
                'Statuses are not the expected in the file.'
            )

        with self.subTest(sub_test='Languages.'):
            self.assertTupleEqual(
                self.database.languages,
                (
                    'Català',
                    'English',
                    'Español',
                    'Suomi',
                    'Русский',
                    'עברית',
                    'සිංහල',
                    '日本語',
                    '繁體中文',
                    '0|\\\\/|G |-|4xx0|2 !!!!111',
                ),
                'Languages are not the expected in the file.',
            )

    def test_02_initialize_with_empty_database_name(self):
        """
        Test if Database raises a TypeError when *database_name* is None.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        database_name = None

        with self.assertRaisesRegex(
            TypeError,
            '"database_name" is not a string.',
        ):
            self.database = Database(
                database_name,
                self.languages_file,
                self.statuses_file,
            )

    def test_03_initialize_with_empty_languages_file(self):
        """
        Test if Database raises a TypeError when *languages_file* is None.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        languages_file = None

        with self.assertRaisesRegex(
            TypeError,
            '"languages_file" is not a string.',
        ):
            self.database = Database(
                self.database_name,
                languages_file,
                self.statuses_file,
            )

    def test_04_initialize_with_empty_statuses_file(self):
        """
        Test if Database raises a TypeError when *statuses_file* is None.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        statuses_file = None

        with self.assertRaisesRegex(
                TypeError,
                '"statuses_file" is not a string.',
        ):
            self.database = Database(
                self.database_name,
                self.languages_file,
                statuses_file,
            )

    def test_05_initialize_with_languages_file_wrong_path(self):
        """
        Test if Database raises a FileNotFoundError when *languages_file* is a path that does not exist.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        languages_file = 'this_should_not_exist_abcdefg.12345'

        with self.assertRaisesRegex(
            FileNotFoundError,
            f'languages_file "{languages_file}" path does not exist.',
        ):
            self.database = Database(
                self.database_name,
                languages_file,
                self.statuses_file,
            )

    def test_06_initialize_with_statuses_file_wrong_path(self):
        """
        Test if Database raises a FileNotFoundError when *statuses_file* is a path that does not exist.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        statuses_file = 'this_should_not_exist_abcdefg.12345'

        with self.assertRaisesRegex(
            FileNotFoundError,
            f'statuses_file "{statuses_file}" path does not exist.',
        ):
            self.database = Database(
                self.database_name,
                self.languages_file,
                statuses_file,
            )

    def test_07_initialize_with_languages_file_not_a_file(self):
        """
        Test if Database raises a FileNotFoundError when *languages_file* is a path to not a file.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        languages_file = 'data'

        with self.assertRaisesRegex(
            FileNotFoundError,
            f'languages_file "{languages_file}" is not a file.',
        ):
            self.database = Database(
                self.database_name,
                languages_file,
                self.statuses_file,
            )

    def test_08_initialize_with_statuses_file_not_a_file(self):
        """
        Test if Database raises a FileNotFoundError when *statuses_file* is a path to not a file.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        statuses_file = 'data'

        with self.assertRaisesRegex(
            FileNotFoundError,
            f'statuses_file "{statuses_file}" is not a file.',
        ):
            self.database = Database(
                self.database_name,
                self.languages_file,
                statuses_file,
            )

    def test_09_initialize_with_expected_parameters_for_second_time(self):
        """
        Test if Database class works as intended with expected parameters initiated a second time.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        prev_read_status = self.database.read_status

        prev_statuses = self.database.statuses

        prev_languages = self.database.languages

        del self.database

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        with self.subTest(sub_test='File still created.'):
            self.assertTrue(
                (
                    os.path.exists(self.database_name)
                ) and (
                    os.path.isfile(self.database_name)
                ),
                'Databse file with name does not exist.'
            )

        with self.subTest(sub_test='Read status.'):
            self.assertEqual(
                self.database.read_status,
                prev_read_status,
                'Read status are not the same".'
            )

        with self.subTest(sub_test='Statuses.'):
            self.assertTupleEqual(
                self.database.statuses,
                prev_statuses,
                'Statuses are not the same.'
            )

        with self.subTest(sub_test='Languages.'):
            self.assertTupleEqual(
                self.database.languages,
                prev_languages,
                'Languages are not the same.',
            )

    def test_10_read_status_property(self):
        """
        Test if "read_status" property returns the read status properly.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        self.assertEqual(
            self.database.read_status,
            'Read',
            '"read_status" does not return expected value.',
        )

    def test_11_statuses_property(self):
        """
        Test if "statuses" property return the statuses properly.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        self.assertTupleEqual(
            self.database.statuses,
            (
                'Currently Reading',
                'Declined',
                'Expugned',
                'Read',
                'To Read',
                'Unfinished',
            ),
            '"statuses" does not return expected values.'
        )

    def test_12_languages_property(self):
        """
        Test if "languages" property return the statuses properly.

        Returns
        -------
        None.

        """
        logging.info('Starting test.')

        self.database = Database(
            self.database_name,
            self.languages_file,
            self.statuses_file,
        )

        self.assertTupleEqual(
            self.database.languages,
            (
                'Català',
                'English',
                'Español',
                'Suomi',
                'Русский',
                'עברית',
                'සිංහල',
                '日本語',
                '繁體中文',
                '0|\\\\/|G |-|4xx0|2 !!!!111',
            ),
            '"languages" does not return expected values.'
        )


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
