# -*- coding: utf-8 -*- noqa
"""
Created on Wed Oct  5 22:08:19 2022

@author: JTS
"""
import sys
import logging
import sqlite3
import traceback
import datetime as dt
import PySimpleGUI as sg
from verify_data import corr_data
from add_archive import add_archive
from error_window import error_window


def add_archive_menu(conn):
    logging.debug("Opening 'Add archive' window.")

    cur = conn.cursor()

    try:
        cur.execute('''
                    SELECT StatusName
                    FROM STATUSES
                    ORDER BY StatusName
            ''')

        statuses = [i[0] for i in cur.fetchall()]

        cur.execute('''
                    SELECT LanguageName
                    FROM LANGUAGES
                    ORDER BY LanguageName
            ''')

        languages = [i[0] for i in cur.fetchall()]

        cur.execute("SELECT MIN(StatusID), StatusName FROM STATUSES")

        read_status = str(cur.fetchone()[1])

    except sqlite3:
        raise KeyError("SQLITE3 error.")

    sg.theme("Python")
    background_colour = sg.theme_background_color()

    left_margin = (13, 1)

    button_add = sg.Button(
        "Add",
        size=(20, 1),
        bind_return_key=True,
        disabled=True,
    )

    button_back = sg.Button(
        "Back",
        size=(20, 1),
    )

    input_title = sg.InputText(
        enable_events=True,
        size=(107, 1),
        key=('Title'),
        focus=True,
    )

    input_author = sg.InputText(
        enable_events=True,
        size=(107, 1),
        key=('AuthorName'),
    )

    input_tags = sg.InputText(
        enable_events=True,
        size=(107, 1),
        key=('TagName'),
    )

    input_external_reference = sg.InputText(
        enable_events=True,
        size=(107, 1),
        key=('ExternalReference'),
    )

    input_publisher = sg.InputText(
        enable_events=True,
        size=(48, 1),
        key=('PublisherName'),
    )

    input_binding = sg.InputText(
        enable_events=True,
        size=(48, 1),
        key=('BindingName'),
    )

    input_word_count = sg.InputText(
        enable_events=True,
        size=(25, 1),
        key=('WordCount'),
    )

    input_chapter_number = sg.InputText(
        enable_events=True,
        size=(25, 1),
        key=('NumberOfChapters'),
    )

    input_rating = sg.InputText(
        enable_events=True,
        size=(25, 1),
        key=('Rating'),
    )

    input_date_added = sg.InputText(
        enable_events=True,
        size=(10, 1),
        key=('DateAdded'),
        readonly=True,
        disabled_readonly_background_color=background_colour,
        default_text=dt.datetime.today().strftime("%Y-%m-%d"),
    )

    calendar_date_added = sg.CalendarButton(
        "Select",
        'DateAdded',
        key='calendar_date_added',
        enable_events=True,
        format='%Y-%m-%d',
    )

    input_original_publishing_date = sg.InputText(
        enable_events=True,
        size=(10, 1),
        key=('OriginallyPublishedDate'),
        readonly=True,
        disabled_readonly_background_color=background_colour,
    )

    calendar_original_publishing_date = sg.CalendarButton(
        "Select",
        'OriginallyPublishedDate',
        key='calendar_original_publishing_date',
        enable_events=True,
        format='%Y-%m-%d',
    )

    input_current_published_version_date = sg.InputText(
        enable_events=True,
        size=(10, 1),
        key=('CurrentVersionDate'),
        readonly=True,
        disabled_readonly_background_color=background_colour,
    )

    calendar_current_published_version_date = sg.CalendarButton(
        "Select",
        'CurrentVersionDate',
        key='calendar_current_published_version_date',
        enable_events=True,
        format='%Y-%m-%d',
    )

    multiline_input_summary = sg.Multiline(
        enable_events=True,
        size=(105, 5),
        key=('Summary'),
        autoscroll=True,
    )

    combo_status = sg.Combo(
        statuses,
        enable_events=True,
        readonly=True,
        size=(45, 1),
        key='StatusName',
    )

    combo_language = sg.Combo(
        languages,
        enable_events=True,
        readonly=True,
        size=(45, 1),
        key='LanguageName',
    )

    multiline_input_review = sg.Multiline(
        enable_events=True,
        size=(105, 3),
        key=('Review'),
        autoscroll=True,
    )

    text_date_read = sg.Text(
        "Date read",
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
        default_text=dt.datetime.today().strftime("%Y-%m-%d"),
    )

    calendar_date_read = sg.CalendarButton(
        "Select",
        'DateRead',
        key='calendar_date_read',
        enable_events=True,
        format='%Y-%m-%d',
        visible=False,
    )

    text_re_read = sg.Text(
        "Times re-read",
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

    layout = [
        [sg.Text("Title❗", size=left_margin), input_title],
        [sg.Text("Authors", size=left_margin), input_author],
        [sg.Text("Tags", size=left_margin), input_tags],
        [sg.Text("External reference", size=left_margin),
         input_external_reference],
        [sg.Text("Publisher", size=left_margin), input_publisher,
         sg.Text("Binding", size=(6, 1)), input_binding],
        [sg.Text("Word Count", size=left_margin), input_word_count,
         sg.Text("Number of chapters", size=(
             15, 1)), input_chapter_number,
         sg.Text("Rating", size=(6, 1)), input_rating],
        [sg.Text("Date added", size=left_margin),
         input_date_added, calendar_date_added,
         sg.Text("Original publishing date"),
         input_original_publishing_date, calendar_original_publishing_date,
         sg.Text("Current published version date"),
         input_current_published_version_date, calendar_current_published_version_date],
        [sg.Text("Summary", size=left_margin), multiline_input_summary],
        [sg.Text("Status", size=left_margin), combo_status,
         sg.Text("Language", size=(8, 1)), combo_language],
        [text_date_read, input_date_read, calendar_date_read,
         text_re_read, input_re_read],
        [sg.Text("Review", size=left_margin), multiline_input_review],
        [sg.Push(), button_add, sg.Push(), button_back, sg.Push()]
    ]

    frame_layout = [
        [sg.VPush()],
        [
            sg.Column(
                [
                    [
                        sg.Frame(
                            "Add archive",
                            layout,
                            expand_x=True,
                            expand_y=True,
                            vertical_alignment='c',
                            background_color=background_colour,
                        )
                    ]
                ],
                justification="center",
                element_justification="center",
            )
        ],
        [sg.VPush()],
    ]

    try:
        window = sg.Window("Add archive", frame_layout,
                           finalize=True, resizable=True)
        window.bring_to_front()
        while True:
            event, values = window.read()
            input_read_state = enable_date_read(read_status, values)
            text_date_read.update(visible=input_read_state)
            input_date_read.update(visible=input_read_state)
            calendar_date_read.update(visible=input_read_state)
            text_re_read.update(visible=input_read_state)
            input_re_read.update(disabled=not input_read_state,
                                 visible=input_read_state)
            button_add.update(disabled=enable_button_add(read_status, values))
            window.finalize()

            if (
                event == "Add"
            ):
                logging.debug("'Add' button pressed.")
                window.disable()
                # window.disappear()
                if corr_data(values):
                    try:
                        conn = add_archive(conn, values)
                    except sqlite3 as message:
                        error_window(message)
                    else:
                        break
                window.enable()
                # window.reappear()
                window.bring_to_front()
            elif (
                event == sg.WIN_CLOSED or event == "Back"
            ):  # if user closes window or clicks cancel
                window.close()
                logging.debug("'Back' button pressed.")
                break
    except:
        exc_tuple = sys.exc_info()
        type_error = str(exc_tuple[0]).split()[1][:-1]
        message = str(exc_tuple[1])
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
        logging.debug("Closing 'Add archive' window.")
        window.close()
        return conn


def enable_date_read(read_status, values):
    return values['StatusName'] == read_status


def enable_button_add(read_status, values):
    obligatory_camps = ('Title', 'AuthorName', 'TagName',
                        'ExternalReference', 'PublisherName', 'BindingName',
                        'WordCount', 'NumberOfChapters',
                        'DateAdded', 'OriginallyPublishedDate',
                        'CurrentVersionDate',
                        'Summary', 'StatusName', 'LanguageName')
    if values['StatusName'] == read_status:
        obligatory_camps += ('DateRead', 'ReRead')
    for key in obligatory_camps:
        if values[key] == "":
            return True

    return False
