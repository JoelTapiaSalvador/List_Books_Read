# -*- coding: utf-8 -*- noqa
"""
Created on Thu Nov  7 18:37:35 2024

@author: JoelT
"""
import logging
import os
import sqlite3


class Database():
    """Database class with the connection to the SQL database."""

    __slots__ = (
        '__connection',
        '__cursor',
        '__database_name',
        '__languages_file',
        '__statuses_file',
    )

###############################################################################
#                             Overloaded Operators                            #

    def __new__(
            cls,
            database_name: str,
            languages_file: str,
            statuses_file: str,
    ):
        """
        Create Database instance.

        Parameters
        ----------
        database_name : str
            Database name.
        languages_file : str
            Path and name of the file containing the languages available of the
            archives.
        statuses_file : str
            Path and name of the file containing the statuses available from
            the archives.

        Raises
        ------
        TypeError
            One of the arguments is of the wrong type.
        FileNotFoundError
            File path are wrong in some way.

        Returns
        -------
        instance : Database
            Database instance.

        """
        if not isinstance(database_name, str):
            logging.error(
                '"database_name" is not a string.'
            )
            raise TypeError('"database_name" is not a string.')

        if not isinstance(languages_file, str):
            logging.error(
                '"languages_file" is not a string.'
            )
            raise TypeError('"languages_file" is not a string.')

        if not isinstance(statuses_file, str):
            logging.error(
                '"statuses_file" is not a string.'
            )
            raise TypeError('"statuses_file" is not a string.')

        if not os.path.exists(languages_file):
            logging.error(
                f'languages_file "{languages_file}" path does not exist.'
            )
            raise FileNotFoundError(
                f'languages_file "{languages_file}" path does not exist.'
            )

        if not os.path.exists(statuses_file):
            logging.error(
                f'statuses_file "{statuses_file}" path does not exist.'
            )
            raise FileNotFoundError(
                f'statuses_file "{statuses_file}" path does not exist.'
            )

        if not os.path.isfile(languages_file):
            logging.error(
                f'languages_file "{languages_file}" is not a file.'
            )
            raise FileNotFoundError(
                f'languages_file "{languages_file}" is not a file.'
            )

        if not os.path.isfile(statuses_file):
            logging.error(
                f'statuses_file "{statuses_file}" is not a file.'
            )
            raise FileNotFoundError(
                f'statuses_file "{statuses_file}" is not a file.'
            )

        instance = super().__new__(cls)
        return instance

    def __init__(
            self,
            database_name: str,
            languages_file: str,
            statuses_file: str,
    ):
        """
        Inicialise the Database.

        Parameters
        ----------
        database_name : string
            Database name.
        languages_file : string
            Path and name of the file containing the languages available of the
            archives.
        statuses_file : string
            Path and name of the file containing the statuses available from
            the archives.

        Returns
        -------
        None.

        """
        logging.info(
            'Initialising SQL database.'
        )

        self.__database_name = database_name

        self.__languages_file = languages_file

        self.__statuses_file = statuses_file

        # Connect to the database
        self.__connection: sqlite3.Connection = sqlite3.connect(
            self.__database_name
        )

        # Set pragma for foreing key
        self.__connection.execute('PRAGMA foreign_keys = ON')
        # self.__connection.execute("PRAGMA encoding = 'UTF-8'")

        # Get the database cursor
        self.__cursor: sqlite3.Cursor = self.__connection.cursor()

        # Create database if it doesn't exist
        self.__create_database()

        logging.info(
            'SQL database initialised.'
        )

    def __repr__(self):
        """
        Representation of the object.

        Returns
        -------
        None.

        """
        representation = (
            f'{self.__class__.__name__}' + '('
            + f'database_name="{self.__database_name}", '
            + f'languages_file="{self.__languages_file}", '
            + f'statuses_file="{self.__statuses_file}"'
            + ')'
        )

        return representation

    def __del__(self):
        """
        Delete Database object.

        Closes connection to database.

        Returns
        -------
        None.

        """
        logging.info('Deleting "Database" instance.')
        self.__cursor.close()

        del self.__cursor

        self.__connection.close()

        del self.__connection

        del self.__languages_file

        del self.__statuses_file

###############################################################################


###############################################################################
#                              Protected Methods                              #

    def __add_internal_values(self):  # noqa
        """
        Add internal values to the database tables if they don't exit already.

        Returns
        -------
        None.

        """
        logging.info(
            'Adding internal values to tables if they do not exist already.'
        )

        with open(self.__statuses_file, "r", encoding="UTF-8") as file:
            statuses = file.readlines()

        if len(statuses) < 1:
            logging.error(
                'Statuses file has no statuses.'
            )
            raise ValueError("Statuses file has no statuses.")

        for i in range(len(statuses)):
            try:
                status = statuses[i][:-1]

                self.__cursor.execute(
                    '''
                    INSERT INTO Statuses (StatusID, StatusName)
                        VALUES
                        (?, ?)
                    ''',
                    (i + 1, status),
                )

                self.__connection.commit()

                logging.debug(
                    f'Status "{status}" did not exist and has been added.'
                )

            except sqlite3.Error as error:
                self.__connection.rollback()
                message = error.args[0]

                if (
                    isinstance(error, sqlite3.IntegrityError)
                ) and (
                    message.split()[0] == "UNIQUE"
                ):
                    logging.debug(
                        f'Status "{status}" already exists in internal' +
                        ' table so it has not been added.'
                    )

                else:
                    raise error

        del status

        with open(self.__languages_file, "r", encoding="UTF-8") as file:
            languages = file.readlines()

        if len(languages) < 1:
            logging.error(
                'Languages file has no languages.'
            )
            raise ValueError('Languages file has no languages.')

        for i in range(len(languages)):
            try:
                language = languages[i][:-1]

                self.__cursor.execute(
                    '''
                    INSERT INTO Languages (LanguageID, LanguageName)
                        VALUES
                        (?, ?)
                    ''',
                    (i + 1, language),
                )

                self.__connection.commit()

                logging.debug(
                    f'Language "{language}" did not exist and has been added.'
                )

            except sqlite3.Error as error:
                self.__connection.rollback()
                message = error.args[0]

                if (
                    isinstance(error, sqlite3.IntegrityError)
                ) and (
                    message.split()[0] == "UNIQUE"
                ):
                    logging.debug(
                        f'Language "{language}" already exists in internal ' +
                        'table so it has not been added.'
                    )

                else:
                    raise error

        del language

        logging.info(
            'Internal values added or already exist.'
        )

    def __create_database(self):
        """
        Create the SQL database if it doesn't exist already.

        Returns
        -------
        None.

        """
        logging.info(
            'Creating Data Base if does not exist already.'
        )

        self.__create_first_level_tables()
        self.__create_second_level_tables()
        self.__add_internal_values()
        self.__connection.commit()

        logging.info(
            'Database created or already exists.'
        )

    def __create_first_level_tables(self):
        """
        Create the first level tables if they don't exist already.

        Returns
        -------
        None.

        """
        logging.info(
            'Creating First Level Tables if they do not exist already.'
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Archives(
                ArchiveID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    ArchiveID >= 1
                ),
                Title  TEXT NOT NULL,
                ExternalReference TEXT NOT NULL,
                DateAdded INTEGER NOT NULL,
                OriginallyPublishedDate INTEGER NOT NULL,
                CurrentVersionDate INTEGER NOT NULL,
                NumberOfChapters INTEGER NOT NULL CHECK (
                    NumberOfChapters >= 1
                ),
                WordCount INTEGER NOT NULL CHECK (
                    WordCount >= 1
                ),
                Summary TEXT NOT NULL,
                Review TEXT,
                Rating INTEGER CHECK (
                    Rating >= 0 AND Rating <= 100
                ),
                LastModification INTEGER NOT NULL,
                CHECK (
                    CurrentVersionDate >=  OriginallyPublishedDate
                )
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Authors(
                AuthorID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    AuthorID >= 1
                ),
                AuthorName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Bindings(
                BindingID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    BindingID >= 1
                ),
                BindingName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Languages(
                LanguageID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    LanguageID >= 1
                ),
                LanguageName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Publishers(
                PublisherID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    PublisherID >= 1
                ),
                PublisherName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Series(
                SerieID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    SerieID >= 1
                ),
                SerieName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Statuses(
                StatusID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    StatusID >= 1
                ),
                StatusName TEXT NOT NULL
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Tags(
                TagID INTEGER PRIMARY KEY ASC NOT NULL CHECK (
                    TagID >= 1
                ),
                TagName TEXT NOT NULL
            );
            '''
        )

        self.__connection.commit()

        logging.info(
            'First Level Tables created or already exist.'
        )

    def __create_second_level_tables(self):
        """
        Create the second level tables if they don't exist already.

        Returns
        -------
        None.

        """
        logging.info(
            'Creating Second Level Tables if they do not exist already.'
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Au_Ar(
                AuthorID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (AuthorID, ArchiveID),
                FOREIGN KEY(AuthorID) REFERENCES Authors(AuthorID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Bi_Ar(
                BindingID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (BindingID, ArchiveID),
                FOREIGN KEY(BindingID) REFERENCES Bindings(BindingID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS La_Ar(
                LanguageID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (ArchiveID),
                FOREIGN KEY(LanguageID) REFERENCES Languages(LanguageID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Pu_Ar(
                PublisherID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (PublisherID, ArchiveID),
                FOREIGN KEY(PublisherID) REFERENCES Publishers(PublisherID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Se_Ar(
                SerieID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PartCode INTEGER NOT NULL,
                PRIMARY KEY (SerieID, ArchiveID, PartCode),
                FOREIGN KEY(SerieID) REFERENCES Series(SerieID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS St_Ar(
                StatusID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                DateRead INTEGER,
                ReRead INTEGER NOT NULL CHECK (ReRead >= 0),
                PRIMARY KEY (ArchiveID),
                FOREIGN KEY(StatusID) REFERENCES Statuses(StatusID),
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID),
                CHECK (
                    StatusID == 1 AND DateRead IS NOT NULL
                )
            );
            '''
        )

        self.__cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Ta_Ar(
                TagID INTEGER NOT NULL,
                ArchiveID INTEGER NOT NULL,
                PRIMARY KEY (TagID, ArchiveID),
                FOREIGN KEY(TagID) REFERENCES Tags(TagID)
                FOREIGN KEY(ArchiveID) REFERENCES Archives(ArchiveID)
            );
            '''
        )

        self.__connection.commit()

        logging.info(
            'Second Level Tables created or already exist.'
        )

    def __verify_add_archive_data(self, data: dict) -> bool:
        """
        Verify if the data to add is in the correct format and values.

        Parameters
        ----------
        data : dictionary(string, string)
            Dictionary with all the data of the archive as key, value pair of
            strings.

        Returns
        -------
        bool
            "True" if the data is in valid format and values "False" if not.

        """
        logging.debug(
            'Verifiyng data values.'
        )

        errors = []

        int_values = ('NumberOfChapters', 'WordCount', 'Rating', 'ReRead')

        if data['OriginallyPublishedDate'] > data['CurrentVersionDate']:
            errors.append(
                (
                    'Current published version date',
                    'Current published version date must be the same or ' +
                    'subsequent to Original publishing date'
                )
            )

        for key in int_values:
            try:
                if data[key] != "":
                    if int(data[key]) < 0:
                        errors.append(
                            (
                                key,
                                'Must be a positive number.'
                            )
                        )
            except ValueError:
                errors.append(
                    (
                        key,
                        'Value must be an integer number.'
                    )
                )

###############################################################################


###############################################################################
#                                  Properties                                 #

    @property  # noqa
    def languages(self) -> tuple:
        """
        Get all the possible languages of the database.

        Returns
        -------
        tuple
            Tuple with all the languages ordered alphabetically.

        """
        self.__cursor.execute(
            '''
            SELECT LanguageName
            FROM LANGUAGES
            ORDER BY LanguageName GLOB '[A-Za-z]*' DESC
            '''
        )

        languages = tuple([i[0] for i in self.__cursor.fetchall()])

        return languages

    @property
    def read_status(self) -> str:
        """
        Get the name of the read status.

        Returns
        -------
        string
            Read status name.

        """
        self.__cursor.execute(
            '''
            SELECT MIN(StatusID), StatusName
            FROM STATUSES
            '''
        )

        read_status = str(self.__cursor.fetchone()[1])

        return read_status

    @property
    def statuses(self) -> tuple:
        """
        Get all the posible status of the database.

        Returns
        -------
        tuple
            Tuple with all the statuses ordered alphabetically.

        """
        self.__cursor.execute(
            '''
            SELECT StatusName
            FROM STATUSES
            ORDER BY StatusName
            '''
        )

        statuses = tuple([i[0] for i in self.__cursor.fetchall()])

        return statuses

###############################################################################


if __name__ == "__main__":
    raise SystemExit(
        'You are executing a module file of the program.' +
        ' Execute the main instead.')
