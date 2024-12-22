# -*- coding: utf-8 -*- noqa
"""
Created on Sun Sep 25 14:02:01 2022

@author: JTS
"""

import sys
import logging
import sqlite3


def create_database(conn):
    """
    Create the SQL database if it doesn't exist already.

    Parameters
    ----------
    conn : TYPE
        DESCRIPTION.

    Returns
    -------
    conn : TYPE
        DESCRIPTION.

    """
    logging.debug("Creating Data Base if doesn't exist already.")
    cur = conn.cursor()
    cur = create_first_level_tables(cur)
    conn.commit()
    cur = create_second_level_tables(cur)
    conn.commit()
    cur = database_values(cur)
    conn.commit()
    logging.debug("Try of inicialization finished.")
    return conn


def create_first_level_tables(cur):
    logging.debug("Creating First Level Tables if doesn't exist already.")

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Archives(
                ArchiveID INTEGER PRIMARY KEY ASC NOT NULL,
                Title  TEXT NOT NULL,
                ExternalReference TEXT NOT NULL,
                DateAdded INTEGER NOT NULL,
                OriginallyPublishedDate INTEGER NOT NULL,
                CurrentVersionDate INTEGER NOT NULL,
                NumberOfChapters INTEGER NOT NULL CHECK (NumberOfChapters >= 1),
                WordCount INTEGER NOT NULL CHECK (WordCount >= 1),
                Summary TEXT NOT NULL,
                Review TEXT,
                Rating INTEGER CHECK (Rating >= 0 AND Rating <= 100),
                LastModification INTEGER NOT NULL,
                CHECK (CurrentVersionDate >=  OriginallyPublishedDate)
                )
                ;
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Authors(
                AuthorID INTEGER PRIMARY KEY ASC NOT NULL,
                AuthorName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Bindings(
                BindingID INTEGER PRIMARY KEY ASC NOT NULL,
                BindingName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Languages(
                LanguageID INTEGER PRIMARY KEY ASC NOT NULL,
                LanguageName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Publishers(
                PublisherID INTEGER PRIMARY KEY ASC NOT NULL,
                PublisherName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Series(
                SerieID INTEGER PRIMARY KEY ASC NOT NULL,
                SerieName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Statuses(
                StatusID INTEGER PRIMARY KEY ASC NOT NULL,
                StatusName TEXT NOT NULL
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Tags(
                TagID INTEGER PRIMARY KEY ASC NOT NULL,
                TagName TEXT NOT NULL
                );
                """
    )
    return cur


def create_second_level_tables(cur):
    logging.debug("Creating Second Level Tables if doesn't exist already.")

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Au_Ar(
                AuthorID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (AuthorID, ArchiveID),
                FOREIGN KEY(AuthorID) REFERENCES Authors(AuthorID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Bi_Ar(
                BindingID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (BindingID, ArchiveID),
                FOREIGN KEY(BindingID) REFERENCES Bindings(BindingID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS La_Ar(
                LanguageID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (ArchiveID),
                FOREIGN KEY(LanguageID) REFERENCES Languages(LanguageID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Pu_Ar(
                PublisherID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (PublisherID, ArchiveID),
                FOREIGN KEY(PublisherID) REFERENCES Publishers(PublisherID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Se_Ar(
                SerieID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PartCode INTEGER NOT NULL,
                PRIMARY KEY (SerieID, ArchiveID, PartCode),
                FOREIGN KEY(SerieID) REFERENCES Series(SerieID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS St_Ar(
                StatusID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                DateRead INTEGER,
                ReRead INTEGER NOT NULL CHECK (ReRead >= 0),
                PRIMARY KEY (ArchiveID),
                FOREIGN KEY(StatusID) REFERENCES Statuses(StatusID),
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID),
                CHECK (StatusID == 1 AND DateRead IS NOT NULL)
                );
                """
    )

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Ta_Ar(
                TagID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (TagID, ArchiveID),
                FOREIGN KEY(TagID) REFERENCES Tags(TagID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
                );
                """
    )
    return cur


def database_values(cur):
    logging.debug(
        "Adding database required values to internal tables if doesn't exist already."
    )

    try:
        cur.execute(
            """
                    INSERT INTO Statuses (StatusID, StatusName)
                        VALUES
                        (1, 'Read'),
                        (2, 'Currently Reading'),
                        (3, 'To Read'),
                        (4, 'Unfinished'),
                        (5, 'Expugned'),
                        (6, 'Declined')
                    """
        )
    except sqlite3.IntegrityError as error:
        exc_tuple = sys.exc_info()
        # type_error = str(exc_tuple[0]).split()[1][:-1]
        message = str(exc_tuple[1])
        if message.split()[0] == "UNIQUE":
            logging.debug(
                "Statuses information already exists in internal table."
            )
        else:
            raise exc_tuple from error

    try:
        with open("languages.txt", "r", encoding="UTF-8") as file:
            lan = file.readlines()
        # tup = ""
        for i in range(len(lan)):
            lan[i] = str((i + 1, lan[i][:-1]))

        cur.execute(
            """
                    INSERT INTO Languages (LanguageID, LanguageName)
                        VALUES """
            + ", ".join(lan)
        )
    except sqlite3.IntegrityError as error:
        exc_tuple = sys.exc_info()
        # type_error = str(exc_tuple[0]).split()[1][:-1]
        message = str(exc_tuple[1])
        if message.split()[0] == "UNIQUE":
            logging.debug(
                "Languages information already exists in internal table."
            )
        else:
            raise exc_tuple from error
    return cur
