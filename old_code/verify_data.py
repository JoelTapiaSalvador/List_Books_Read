# -*- coding: utf-8 -*- noqa
"""
Created on Mon Oct  3 19:08:21 2022

@author: JTS
"""
import logging
from error_window import error_window


def corr_data(values):
    logging.debug("Verifiyng data values.")

    errors = []

    int_values = ('NumberOfChapters', 'WordCount', 'Rating', 'ReRead')

    if values['OriginallyPublishedDate'] > values['CurrentVersionDate']:
        errors.append(("Current published version date",
                      'Current published version date must be the same or subsequent to Original publishing date'))

    for key in int_values:
        try:
            if values[key] != "":
                if int(values[key]) < 0:
                    errors.append((key, "Must be a positive number."))
        except ValueError:
            errors.append((key, "Value must be an integer number."))

    if len(errors) == 0:
        return True
    error_window(errors)
    return False
