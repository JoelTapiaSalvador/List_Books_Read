# -*- coding: utf-8 -*- noqa
"""
Created on Thu Sep 29 22:37:44 2022

@author: JTS
"""
import sys
import logging
import sqlite3
import traceback
import PySimpleGUI as sg


def add_archive(conn, values):
    logging.debug("Adding archive.")

    values = correct_value_dictionary(values)

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Archives WHERE Title = " +
                    values['Title'] + " ORDER BY LastModification DESC")
        result = cur.fetchall()
        if len(result) != 0:
            choice, _ = sg.Window('Continue?', [
                [sg.T('Archive with titile already exists. Do you want to continue?')],
                [sg.Push(), sg.Yes(s=10), sg.Push(), sg.No(s=10), sg.Push()]
            ], disable_close=True, disable_minimize=True, keep_on_top=True,
                grab_anywhere=True, no_titlebar=True, modal=True,
                text_justification='center').read(close=True)
            if choice == 'No':
                return conn

        cur, ArchiveID = add_Archives_obligatiry_information(cur, values)

        cur = add_Archives_optional_information(cur, values, ArchiveID)

        cur = add_Language(cur, values, ArchiveID)

        cur = add_Status(cur, values, ArchiveID)

        cur = add_Listing_Values(cur, values, ArchiveID)

        conn.commit()

    except sqlite3.OperationalError:
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
    return conn


def correct_value_dictionary(values):
    for i in ('cal_date_added', 'cal_original_publishing_date',
              'cal_current_published_version_date', 'cal_date_read'):
        del values[i]

    for i in ('Title', 'ExternalReference', 'DateAdded', 'OriginallyPublishedDate', 'CurrentVersionDate', 'Summary', 'StatusName', 'LanguageName', 'DateRead', 'Review'):
        values[i] = "'" + values[i] + "'"

    for i in ('AuthorName', 'TagName', 'PublisherName', 'BindingName'):
        values[i] = values[i].replace(', ', ',')
        values[i] = tuple(["'" + j + "'" for j in values[i].split(",")])

    return values


def add_Archives_obligatiry_information(cur, values):
    cur.execute("INSERT INTO Archives ("
                + "Title, "
                + "ExternalReference, "
                + "DateAdded, "
                + "OriginallyPublishedDate, "
                + "CurrentVersionDate, "
                + "NumberOfChapters, "
                + "WordCount, "
                + "Summary, "
                + "LastModification"
                + ") VALUES (" + values['Title'] + ", " + values['ExternalReference'] + ", " + "unixepoch(" + values[
                    'DateAdded'] + "), unixepoch(" + values['OriginallyPublishedDate'] + "), unixepoch(" + values['CurrentVersionDate'] + "), " + values['NumberOfChapters'] + ", " + values['WordCount'] + ", " + values['Summary'] + ", unixepoch())")

    cur.execute("SELECT ArchiveID FROM Archives WHERE Title=" +
                values['Title'] + " ORDER BY LastModification DESC")

    archiveID = str(cur.fetchone()[0])
    return cur, archiveID


def add_Archives_optional_information(cur, values, ArchiveID):
    for i in ('Rating', 'Review'):
        if values[i] != '':
            cur.execute("UPDATE Archives SET " + i + " = " +
                        values[i] + " WHERE ArchiveID = " + str(ArchiveID))
    return cur


def add_Language(cur, values, ArchiveID):
    cur.execute(
        "SELECT LanguageID FROM Languages WHERE LanguageName = " + values['LanguageName'])
    LanguageID = str(cur.fetchone()[0])
    cur.execute("INSERT INTO La_Ar (ArchiveID, LanguageID) VALUES (" +
                ArchiveID + ", " + LanguageID + ")")
    return cur


def add_Listing_Values(cur, values, ArchiveID):
    for i in ('Authors', 'Bindings', 'Publishers', 'Tags'):
        for j in values[i[:-1] + "Name"]:
            cur.execute("SELECT " + i[:-1] + "ID" + " FROM " +
                        i + " WHERE " + i[:-1] + "Name" + " = " + j)
            ID = cur.fetchall()
            while len(ID) == 0:
                cur.execute("INSERT INTO " + i +
                            " (" + i[:-1] + "Name) VALUES (" + j + ")")
                cur.execute("SELECT " + i[:-1] + "ID" + " FROM " +
                            i + " WHERE " + i[:-1] + "Name" + " = " + j)
                ID = cur.fetchall()
            cur.execute("INSERT INTO " + i[:2] + "_Ar (ArchiveID,  " + i[:-1] + "ID) VALUES (" +
                        ArchiveID + ", " + str(ID[0][0]) + ")")
    return cur


def add_Status(cur, values, ArchiveID):
    cur.execute("SELECT MIN(StatusID), StatusName FROM STATUSES")

    read_status = cur.fetchone()

    if values['StatusName'] == "'" + read_status[1] + "'":
        cur.execute(
            "INSERT INTO St_Ar (StatusID, ArchiveID, DateRead, ReRead) VALUES (" + str(read_status[0]) + ", " + ArchiveID + ", unixepoch(" + values['DateRead'] + "), " + values['ReRead'] + ")")
        return cur
    cur.execute("SELECT StatusID FROM Statuses WHERE StatusName = " +
                values['StatusName'])

    StatusID = str(cur.fetchone()[0])

    cur.execute(
        "INSERT INTO St_Ar (StatusID, ArchiveID, ReRead) VALUES (" + StatusID + ", " + ArchiveID + ", " + values['ReRead'] + ")")
    return cur
