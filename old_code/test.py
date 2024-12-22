# -*- coding: utf-8 -*- noqa
"""
Created on Sat Oct  8 13:37:08 2022

@author: JTS
"""
import os
import sys
import logging
import sqlite3
import traceback
import PySimpleGUI as sg
from create_database import create_database
from add_archive import add_archive
# from add_archive import correct_value_dictionary

try:
    expected_result = [(1,
                        'Test',
                        'jts.com/books/test',
                        98,
                        '2022-10-29',
                        '2022-10-10',
                        '2022-10-31',
                        '2022-10-08',
                        'Read',
                        'Català',
                        12,
                        145873,
                        'Testing book.',
                        None,
                        None,
                        1665258147)]
    values = {'Title': 'Test',
              'AuthorName': 'JTS, Joel',
              'TagName': 'Programing, Test',
              'ExternalReference': 'jts.com/books/test',
              'PublisherName': 'JTS Publishing',
              'BindingName': 'Kindle, PDF',
              'WordCount': '145873',
              'NumberOfChapters': '12',
              'Rating': '98',
              'DateAdded': '2022-10-08', 'cal_date_added': '',
              'OriginallyPublishedDate': '2022-10-10', 'cal_original_publishing_date': '',
              'CurrentVersionDate': '2022-10-29', 'cal_current_published_version_date': '',
              'Summary': 'Testing book.',
              'StatusName': 'Read', 'LanguageName': 'Català',
              'DateRead': '2022-10-31', 'cal_date_read': '',
              'ReRead': '0',
              'Review': 'Good.'}
    test = {'Title': 'Test', 'AuthorName': 'JTS, Joel',
            'TagName': 'Programing, Test',
            'ExternalReference': 'jts.com/books/test',
            'PublisherName': 'JTS Publishing', 'BindingName': 'Kindle, PDF',
            'WordCount': '145873', 'NumberOfChapters': '12', 'Rating': '98',
            'DateAdded': '2022-10-08', 'cal_date_added': '',
            'OriginallyPublishedDate': '2022-10-10',
            'cal_original_publishing_date': '',
            'CurrentVersionDate': '2022-10-29',
            'cal_current_published_version_date': '',
            'Summary': 'Testing book.', 'StatusName': 'Read',
            'LanguageName': 'Català', 'DateRead': '2022-10-31',
            'cal_date_read': '', 'ReRead': '0', 'Review': 'Good.'}
    DATABASE_NAME = 'archive_database'
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn = create_database(conn)
    # conn = add_archive(conn, values)
    cur = conn.cursor()
    # cur.execute(
    # "SELECT Ar.ArchiveID, Ar.Title, Ar.ExternalReference, Ar.Rating, date(Ar.CurrentVersionDate, 'unixepoch', 'localtime'), date(Ar.OriginallyPublishedDate, 'unixepoch', 'localtime'), date(St_Ar.DateRead, 'unixepoch', 'localtime'), date(Ar.DateAdded, 'unixepoch', 'localtime'), St.StatusName, La.LanguageName  FROM Archives AS Ar, Languages AS La, La_Ar, Statuses AS St, St_Ar WHERE Ar.ArchiveID = La_Ar.ArchiveID AND La_Ar.LanguageID = La.LanguageID AND Ar.ArchiveID = St_Ar.ArchiveID AND St_Ar.StatusID = St.StatusID")
    # result_1 = cur.fetchall()
    # cur.execute("SELECT * FROM Archives")
    # result_2 = cur.fetchall()
    # t = correct_value_dictionary(values)
finally:
    conn.close()
    os.remove("archive_database")
