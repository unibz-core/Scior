""" General auxiliary functions. """
import os
import platform
from datetime import datetime

import psutil


def has_duplicates(input_list):
    """ Check if given list contains any duplicated element """
    if len(input_list) == len(set(input_list)):
        return False
    else:
        return True


def remove_duplicates(input_list):
    """ Remove duplicated elements from a list. """

    output_list = [*set(input_list)]

    return output_list


def lists_intersection(list1, list2):
    """ Returns the intersection of two lists. """
    temp = set(list2)
    list3 = [value for value in list1 if value in temp]
    return list3


def lists_subtraction(list1, list2):
    """ Returns the subtraction between two lists. """

    list3 = list(set(list1) - set(list2))

    return list3


def get_date_time():
    """ Return a string in a specified format with date and time.
    Format example: 2022.10.23-14.43
    """

    now = datetime.now()
    date_time = now.strftime("%Y.%m.%d-%H.%M.%S")

    return date_time


def get_computer_specifications():
    """ Returns a dictionary with basic information about the computer specifications """

    try:
        computer_specs = {}
        computer_specs['Python version'] = platform.python_version()
        computer_specs['Operating System'] = platform.system() + " " + platform.release() + " - v" + platform.version()
        computer_specs['Processor'] = platform.processor() + " (" + platform.machine() + ")"
        computer_specs['Installed RAM'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return computer_specs

    except Exception as error:
        print(f"Failed to collect the computer specifications. Program aborted.\n"
              f"System error message is: {error}")
        exit(1)


def create_directory_if_not_exists(directory_path: str) -> None:
    """ Checks if a directory exists.
        If it does, do nothing.
        If it does not, create it.
    """

    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except OSError as error:
        print(f"Could not create {directory_path} directory. Exiting program.")
        raise OSError(error)
