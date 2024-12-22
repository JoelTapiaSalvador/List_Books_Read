# -*- coding: utf-8 -*- noqa
"""
Created on Tue Oct  4 10:02:44 2022

@author: JTS
"""
import sys
import logging
import sqlite3
import datetime as dt
import PySimpleGUI as sg


def error_window(errors):
    logging.debug("Opening 'Error' window.")

    left_margin = (22, 1)

    b_ok = sg.Button("Ok", size=(20, 1), bind_return_key=True)

    errors_layout = [[sg.VPush()], [sg.Column([[sg.Text(error[0], size=left_margin), sg.Multiline(
        disabled=True, default_text=error[1], size=(97, 5))] for error in errors], scrollable=True, vertical_scroll_only=True, size=(900, 400), justification="center", element_justification="center", vertical_alignment='center', expand_x=True,	expand_y=True)], [sg.VPush()]]
    errors_layout.append([b_ok])

    layout = [
        [sg.VPush()],
        [sg.Column(errors_layout, justification="center",
                   element_justification="center")],
        [sg.VPush()]]

    try:
        sg.theme("Python")
        window = sg.Window("Error", layout,
                           finalize=True, resizable=True)
        window.bring_to_front()
        while True:
            event, values = window.read()
            if (
                event == sg.WIN_CLOSED or event == "Ok"
            ):  # if user closes window or clicks cancel
                window.close()
                logging.debug("'Exit' button pressed.")
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
    finally:
        logging.debug("Closing 'Add archive' window.")
        window.close()
