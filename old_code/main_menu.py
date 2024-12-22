# -*- coding: utf-8 -*- noqa
"""
Created on Wed Sep 28 23:08:53 2022

@author: JoelT
"""

import time
import logging
import PySimpleGUI as sg
from add_archive_menu import add_archive_menu


def main_menu(conn):
    logging.debug("Opening 'Main menu' window.")

    sg.theme("Python")
    background_colour = sg.theme_background_color()

    max_text_but = 30

    button_add = sg.Button(
        "Add archive",
        size=(max_text_but, 1),
        bind_return_key=True,
    )

    button_search = sg.Button(
        "Search archive",
        size=(max_text_but, 1),
    )

    button_export = sg.Button(
        "Export database to CSV file",
        size=(max_text_but, 1),
        tooltip="Create a .csv document with all the information of the database."
    )

    button_settings = sg.Button(
        "Settings",
        size=(max_text_but, 1),
    )

    button_exit = sg.Button(
        "Exit",
        size=(max_text_but, 1),
    )

    layout = [[sg.VPush()], [sg.Sizer(h_pixels=348, v_pixels=52)],
              [sg.Column(
                  [[sg.Sizer(h_pixels=20, v_pixels=26), button_add,
                    sg.Sizer(h_pixels=20, v_pixels=26)]],
                  justification="center",
                  element_justification="center",
              )],
              [sg.Column(
                  [[sg.Sizer(h_pixels=20, v_pixels=26), button_search,
                    sg.Sizer(h_pixels=20, v_pixels=26)]],
                  justification="center",
                  element_justification="center",
              )],
              [sg.Column(
                  [[sg.Sizer(h_pixels=20, v_pixels=26), button_export,
                    sg.Sizer(h_pixels=20, v_pixels=26)]],
                  justification="center",
                  element_justification="center",
              )],
              [sg.Column(
                  [[sg.Sizer(h_pixels=20, v_pixels=26), button_settings,
                    sg.Sizer(h_pixels=20, v_pixels=26)]],
                  justification="center",
                  element_justification="center",
              )],
              [sg.Column(
                  [[sg.Sizer(h_pixels=20, v_pixels=26), button_exit,
                    sg.Sizer(h_pixels=20, v_pixels=26)]],
                  justification="center",
                  element_justification="center",
              )], [sg.Sizer(h_pixels=348, v_pixels=52)], [sg.VPush()]
              ]

    frame_layout = [
        [sg.VPush()],
        [sg.Column([[sg.Frame("Archive Database", layout, expand_x=True,
                              expand_y=True, vertical_alignment='c',
                              background_color=background_colour)]
                    ],
                   justification="center",
                   element_justification="center",
                   )], [sg.VPush()]]

    try:
        window = sg.Window("Archive Database", frame_layout,
                           finalize=True, resizable=True)
        window.bring_to_front()
        while True:
            event, values = window.read()
            if (
                event == "Add archive"
            ):
                logging.debug('Add archive" button pressed.')
                window.disable()
                # window.disappear()
                conn = add_archive_menu(conn)
                # window.reappear()
                window.enable()
                window.bring_to_front()
            elif (
                event == sg.WIN_CLOSED or event == "Exit"
            ):  # if user closes window or clicks cancel
                logging.debug('"Exit" button pressed.')
                break
    finally:
        logging.debug('Closing "Main menu" window.')
        window.close()
        return conn
