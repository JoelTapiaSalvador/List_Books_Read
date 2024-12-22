# -*- coding: utf-8 -*- noqa
"""
Created on Fri Sep 23 19:18:02 2022

@author: JTS
"""
import sys
import sqlite3
import logging
import traceback

from database import Database
from main_menu import main_menu
from create_database import create_database


DATABASE_NAME = 'archive_database'


def main():
    """
    Execute main logic.

    Returns
    -------
    None.

    """

    logging

    logging.basicConfig(
        filename="logging.log",
        filemode="w",
        level=logging.DEBUG,
        force=True,
        format='[%(asctime)s] %(levelname)s:\n\tModule: "%(module)s"\n\tFunction: "%(funcName)s"\n\tLine: %(lineno)d\n\t\t%(message)s\n',
    )

    try:
        database = Database(DATABASE_NAME)
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
        # conn.execute("DSQLITE_MAX_LENGTH = 2147483647")
        conn = create_database(conn)
        conn = main_menu(conn)
    except:
        exc_tuple = sys.exc_info()
        type_error = str(exc_tuple[0]).split()[1][:-1]
        message = str(exc_tuple[1])

        logging.critical(traceback.format_exc()[
                         :-1].replace("  ", "\t").replace("\n", "\n\t\t"))

        print(
            ("An error has occured.")
            + "\n\t"
            + ("Error Type:")
            + " \n\t\t"
            + type_error
            + "\n\t"
            + ("Error message:")
            + " \n\t\t"
            + message
        )
        traceback.print_exc()

    finally:
        conn.commit()
        conn.close()
        logging.shutdown()


if __name__ == "__main__":
    main()
