# -*- coding: utf-8 -*- noqa
"""
Created on Sun Nov 10 01:38:57 2024

@author: JTS
"""
import logging

import PySimpleGUI as sg

from datetime import datetime

# Needed because we store methods as attributes and if not used, Garbage
# Collector sees there are more than one reference to the object and del will
# never work.
# See https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s15.html
from weakref import WeakMethod

from .database import Database


class WindowAddArchive():
    """Creates and manages the window to add archives."""

    __slots__ = (
        '__database',
        '__enable_date_read',
        '__enable_button_add',
        '__event',
        '__inputs',
        '__languages',
        '__obligatory_camps',
        '__read_status',
        '__statuses',
        '__theme',
        '__updatables',
        '__weakref__',  # Slot needed for storing the week references
        '__window',
        '__window_layout',
    )

###############################################################################
#                             Overloaded Operators                            #

    def __new__(  # noqa
            cls,
            database: Database,
            theme: str = 'Python',
    ):
        """
        Create WindowAddArchive instance.

        Parameters
        ----------
        database : Database
            Database containing all archive information.
        theme : str, optional
            GUI theme. The default is 'Python'.

        Raises
        ------
        TypeError
            One of the arguments is of the wrong type.
        ValueError
            Theme provided is not available.

        Returns
        -------
        instance : WindowAddArchive
            WindowAddArchive.

        """
        # Controlling inputs
        if not isinstance(database, Database):
            logging.error('"database" is not a Database')
            raise TypeError('"database" is not a Database')

        if not isinstance(theme, str):
            logging.error('"theme" is not a string.')
            raise TypeError('"theme" is not a string.')

        if theme not in sg.theme_list():
            logging.error('"theme" is not an available theme.')
            raise ValueError('"theme" is not an available theme.')

        instance = super().__new__(cls)
        return instance

    def __init__(
            self,
            database: Database,
            theme: str = 'Python',
    ):
        logging.info('Initializing WindowAddArchive.')
        # Disable PySimpleGUI  debugger because it keeps references to the
        # object that avoid it's proper deletion.
        sg.set_options(debug_win_size=False)

        # Atributes
        self.__database = database
        logging.debug(f'Database:\n\t\t\t{self.__database}')

        self.__theme = theme

        self.__languages = self.__database.languages
        logging.debug(f'Languages available:\n\t\t\t{self.__languages}')

        self.__read_status = self.__database.read_status
        logging.debug(f'Read status: {self.__read_status}')

        self.__statuses = self.__database.statuses
        logging.debug(f'Statuses:\n\t\t\t{self.__statuses}')

        self.__enable_date_read = False

        self.__enable_button_add = False

        # Key of the input fields that have obligatory camps, second elemet is
        # what determines how to check if is obligatory.
        self.__obligatory_camps = (
            ('Title', WeakMethod(self.__get_true), False),
            ('AuthorName', WeakMethod(self.__get_true), False),
            ('TagName', WeakMethod(self.__get_true), False),
            ('ExternalReference', WeakMethod(self.__get_true), False),
            ('PublisherName', WeakMethod(self.__get_true), False),
            ('BindingName', WeakMethod(self.__get_true), False),
            ('WordCount', WeakMethod(self.__get_true), False),
            ('NumberOfChapters', WeakMethod(self.__get_true), False),
            ('DateAdded', WeakMethod(self.__get_true), False),
            ('OriginallyPublishedDate', WeakMethod(self.__get_true), False),
            ('CurrentVersionDate', WeakMethod(self.__get_true), False),
            ('Summary', WeakMethod(self.__get_true), False),
            ('StatusName', WeakMethod(self.__get_true), False),
            ('LanguageName', WeakMethod(self.__get_true), False),
            ('DateRead', WeakMethod(self.__get_enable_date_read), False),
            ('ReRead', WeakMethod(self.__get_enable_date_read), False),
        )

        # Setting window
        sg.theme(self.__theme)

        background_colour = sg.theme_background_color()

        left_margin = (14, 1)

        # Title input
        text_title = sg.Text('Title*', size=left_margin)

        input_title = sg.InputText(
            enable_events=True,
            size=(110, 1),
            key=('Title'),
            focus=True,
        )

        # Author input
        text_author = sg.Text('Authors*', size=left_margin)

        input_author = sg.InputText(
            enable_events=True,
            size=(110, 1),
            key=('AuthorName'),
        )

        # Tags input
        text_tags = sg.Text('Tags*', size=left_margin)

        input_tags = sg.InputText(
            enable_events=True,
            size=(110, 1),
            key=('TagName'),
        )

        # External reference input
        text_external_reference = sg.Text(
            'External reference*',
            size=left_margin)

        input_external_reference = sg.InputText(
            enable_events=True,
            size=(110, 1),
            key=('ExternalReference'),
        )

        # Publisher input
        text_publisher = sg.Text('Publisher*', size=left_margin)

        input_publisher = sg.InputText(
            enable_events=True,
            size=(48, 1),
            key=('PublisherName'),
        )

        # Binding input
        text_binding = sg.Text('Binding*', size=(6, 1))

        input_binding = sg.InputText(
            enable_events=True,
            size=(48, 1),
            key=('BindingName'),
        )

        # Word Count input
        text_word_count = sg.Text('Word Count*', size=left_margin)

        input_word_count = sg.InputText(
            enable_events=True,
            size=(26, 1),
            key=('WordCount'),
        )

        # Number of Chapters input
        text_number_chapters = sg.Text('Number of chapters*', size=(15, 1))

        input_number_chapters = sg.InputText(
            enable_events=True,
            size=(26, 1),
            key=('NumberOfChapters'),
        )

        # Rating input
        text_rating = sg.Text('Rating', size=(6, 1))

        input_rating = sg.InputText(
            enable_events=True,
            size=(26, 1),
            key=('Rating'),
        )

        # Date Added input
        text_date_added = sg.Text('Date added*', size=left_margin)

        input_date_added = sg.InputText(
            enable_events=True,
            size=(10, 1),
            key=('DateAdded'),
            readonly=True,
            disabled_readonly_background_color=background_colour,
            default_text=datetime.today().strftime('%Y-%m-%d'),
        )

        calendar_date_added = sg.CalendarButton(
            'Select',
            'DateAdded',
            key='calendar_date_added',
            enable_events=True,
            format='%Y-%m-%d',
        )

        # Original Publishing Date input
        text_original_publishing_date = sg.Text('Original publishing date*')

        input_original_publishing_date = sg.InputText(
            enable_events=True,
            size=(10, 1),
            key=('OriginallyPublishedDate'),
            readonly=True,
            disabled_readonly_background_color=background_colour,
        )

        calendar_original_publishing_date = sg.CalendarButton(
            'Select',
            'OriginallyPublishedDate',
            key='calendar_original_publishing_date',
            enable_events=True,
            format='%Y-%m-%d',
        )

        # Current Version Publishing Date input
        text_current_version_publishing_date = sg.Text(
            'Current version publishing date*'
        )

        input_current_published_version_date = sg.InputText(
            enable_events=True,
            size=(10, 1),
            key=('CurrentVersionDate'),
            readonly=True,
            disabled_readonly_background_color=background_colour,
        )

        calendar_current_published_version_date = sg.CalendarButton(
            'Select',
            'CurrentVersionDate',
            key='calendar_current_published_version_date',
            enable_events=True,
            format='%Y-%m-%d',
        )

        # Summary input
        text_summary = sg.Text('Summary*', size=left_margin)

        multiline_input_summary = sg.Multiline(
            enable_events=True,
            size=(107, 5),
            key=('Summary'),
            autoscroll=True,
        )

        # Status input
        text_status = sg.Text('Status*', size=left_margin)

        combo_status = sg.Combo(
            self.__statuses,
            enable_events=True,
            readonly=True,
            size=(46, 1),
            key='StatusName',
        )

        # Language input
        text_language = sg.Text('Language*', size=(8, 1))

        combo_language = sg.Combo(
            self.__languages,
            enable_events=True,
            readonly=True,
            size=(46, 1),
            key='LanguageName',
        )

        # Date Read input
        text_date_read = sg.Text(
            'Date read*',
            size=left_margin,
            visible=False,
        )

        input_date_read = sg.InputText(
            enable_events=True,
            size=(10, 1),
            key=('DateRead'),
            readonly=True,
            disabled_readonly_background_color=background_colour,
            visible=False,
            default_text=datetime.today().strftime('%Y-%m-%d'),
        )

        calendar_date_read = sg.CalendarButton(
            'Select',
            'DateRead',
            key='calendar_date_read',
            enable_events=True,
            format='%Y-%m-%d',
            visible=False,
        )

        # Times Re-Read input
        text_re_read = sg.Text(
            'Times re-read*',
            visible=False,
        )

        input_re_read = sg.InputText(
            enable_events=True,
            size=(22, 1),
            key=('ReRead'),
            disabled=True,
            visible=False,
            default_text=0,
        )

        # Review input
        text_review = sg.Text('Review', size=left_margin)

        multiline_input_review = sg.Multiline(
            enable_events=True,
            size=(105, 3),
            key=('Review'),
            autoscroll=True,
        )

        # Add button
        button_add = sg.Button(
            'Add',
            size=(20, 1),
            bind_return_key=True,
            disabled=True,
        )

        # Back button
        button_back = sg.Button(
            'Back',
            size=(20, 1),
        )

        # Frame layout
        frame_layout = [
            [text_title, input_title],
            [text_author, input_author],
            [text_tags, input_tags],
            [text_external_reference, input_external_reference],
            [text_publisher, input_publisher, text_binding, input_binding],
            [
                text_word_count, input_word_count,
                text_number_chapters,
                input_number_chapters,
                text_rating, input_rating
            ],
            [
                text_date_added,
                input_date_added,
                calendar_date_added,
                text_original_publishing_date,
                input_original_publishing_date,
                calendar_original_publishing_date,
                text_current_version_publishing_date,
                input_current_published_version_date,
                calendar_current_published_version_date
            ],
            [text_summary, multiline_input_summary],
            [text_status, combo_status, text_language, combo_language],
            [
                text_date_read,
                input_date_read,
                calendar_date_read,
                text_re_read,
                input_re_read
            ],
            [text_review, multiline_input_review],
            [sg.Push(), button_add, sg.Push(), button_back, sg.Push()],
        ]

        logging.debug(f'Frame layout:\n{frame_layout}')

        # Window layout
        self.__window_layout = [
            [sg.VPush()],
            [
                sg.Column(
                    [
                        [
                            sg.Frame(
                                'Add archive',
                                frame_layout,
                                expand_x=True,
                                expand_y=True,
                                vertical_alignment='c',
                                background_color=background_colour,
                            )
                        ]
                    ],
                    justification='center',
                    element_justification='center',
                )
            ],
            [sg.VPush()],
        ]

        # Updatable elements and what attributes and how the updates are
        # determined
        self.__updatables = (
            (text_date_read, (
                ('visible', WeakMethod(self.__get_enable_date_read), False),
            )),
            (input_date_read, (
                ('visible', WeakMethod(self.__get_enable_date_read), False),
            )),
            (calendar_date_read, (
                ('visible', WeakMethod(self.__get_enable_date_read), False),
            )),
            (text_re_read, (
                ('visible', WeakMethod(self.__get_enable_date_read), False),
            )),
            (input_re_read, (
                ('disabled', WeakMethod(self.__get_enable_date_read), True),
                ('visible', WeakMethod(self.__get_enable_date_read), False),
            )),
            (button_add, (
                ('disabled', WeakMethod(self.__get_enable_button_add), True),
            )),
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
            + f'database={self.__database}, '
            + f'theme="{self.__theme}", '
            + ')'
        )

        return representation

    def __del__(self):
        """
        Delete WindowAddArchive object.

        Returns
        -------
        None.

        """
        logging.info('Deleting "WindowAddArchive" instance.')
        if not self.__window.is_closed():
            self.__window.close()
            self.__empty_sg_debugger()

        del self.__window
        del self.__database

        del self.__enable_date_read
        del self.__enable_button_add
        del self.__event
        del self.__inputs
        del self.__languages
        del self.__obligatory_camps
        del self.__read_status
        del self.__statuses
        del self.__theme
        del self.__updatables
        del self.__window_layout

###############################################################################


###############################################################################
#                              Protected Methods                              #

    def __empty_sg_debugger(self):  # noqa
        logging.debug('Emptying PySimpleGUI debugger.')
        debugger = sg.PySimpleGUI._Debugger.debugger
        if debugger is not None:
            debugger.locals = {}

    def __check_enable_date_read(self) -> bool:
        return self.__inputs['StatusName'] == self.__read_status

    def __check_enable_button_add(self) -> bool:
        for key, check, inverse in self.__obligatory_camps:
            if check(inverse):
                if self.__inputs[key] == "":
                    return False
        return True

    def __get_enable_date_read(self, inverse: bool = False) -> bool:
        return inverse ^ self.__enable_date_read

    def __get_enable_button_add(self, inverse: bool = False) -> bool:
        return inverse ^ self.__enable_button_add

    def __get_true(self, inverse: bool = False) -> False:
        return inverse ^ True

###############################################################################


###############################################################################
#                                Public Methods                               #

    def render(self):  # noqa
        """
        Render window.

        Returns
        -------
        None.

        """
        logging.info('Rendering window.')
        self.__window = sg.Window(
            'Add archive',
            self.__window_layout,
            finalize=True,
            resizable=True,
            # Disable PySimpleGUI debugger because it keeps references to the
            # object that avoid it's proper deletion.
            debugger_enabled=False,
        )
        self.__empty_sg_debugger()
        self.__window.disable_debugger()
        self.__empty_sg_debugger()
        self.__window.bring_to_front()
        self.__empty_sg_debugger()

    def update(self) -> bool:
        """
        Update window.

        Returns
        -------
        bool
            Return if the window is still open (True) or if it has been closed
            (False).

        """
        logging.info('Updating window.')
        # Get events and inputs from the window
        self.__event, self.__inputs = self.__window.read()
        self.__empty_sg_debugger()

        # Check for events
        if (
            self.__event == sg.WIN_CLOSED or self.__event == 'Back'
        ):  # if user closes window or clicks cancel
            logging.info('Back button pressed.')
            self.__window.close()
            self.__empty_sg_debugger()

            # Return the window is no longer open
            return False
        if (
            self.__event == 'Add'
        ):
            logging.info('Add button pressed.')
            self.__window.disable()
            self.__empty_sg_debugger()
            # window.disappear()

            # Request to add to the database
            # TODO

            self.__window.enable()
            self.__empty_sg_debugger()
            # window.reappear()
            self.__window.bring_to_front()
            self.__empty_sg_debugger()

        # Check if some inputs are shown depending on other inputs
        self.__enable_date_read = self.__check_enable_date_read()

        # Check if Add Button can be enabled depending on the inputs
        self.__enable_button_add = self.__check_enable_button_add()

        # Update elements depending on the checks
        for element, params in self.__updatables:
            kwargs = {key: check(inverse)
                      for key, check, inverse in params}
            element.update(**kwargs)

        # Update the window
        self.__window.finalize()
        self.__empty_sg_debugger()

        # Return the window is still open
        return True

###############################################################################


if __name__ == "__main__":
    raise SystemExit(
        'You are executing a module file of the program.' +
        ' Execute the main instead.')
