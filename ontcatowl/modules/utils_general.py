""" General auxiliary functions. """
from datetime import datetime


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
