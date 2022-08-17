""" Implements functions for GUFO Data.
- Loading GUFO Data used for the evaluations from a YAML file and creates an output dictionary.
- Validate if the loaded data is correct.
"""

import time

import yaml
from yaml import SafeLoader

from modules.logger_config import initialize_logger
from modules.utils_general import has_duplicates

# TODO (@pedropaulofb): These values must be updated when the YAML file is updated.
NUMBER_CLASSES_TYPES = 14
NUMBER_CLASSES_INDIVIDUALS = 13


def initialize_gufo_dictionary():
    """ Loads GUFO Data from a YAML resource file and returns a multi-level dictionary
        The dictionary contains:
            - 1st level keys: hierarchies (types or individuals)
            - 2nd level keys: classes belonging to the hierarchies
            - 3rd level: three lists of strings (is_list, can_list, not_list) with related classes
    """

    logger = initialize_logger()

    gufo_data_file = "../resources/gufo_data.yaml"
    logger.debug(f"Loading {gufo_data_file} file...")

    try:
        with open(gufo_data_file) as f:
            loaded_gufo_data = yaml.load(f, Loader=SafeLoader)
            logger.debug(f"{gufo_data_file} file successfully loaded.")
    except OSError:
        logger.error(f"Could not load {gufo_data_file} file. Exiting program.")
        exit(1)

    st = time.perf_counter()
    validate_gufo_data(loaded_gufo_data)
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"Execution time: {elapsed_time} seconds.")

    return loaded_gufo_data


def validate_gufo_data(gufo_data):
    """ Validate the GUFO data loaded from the YAML resource file. """

    logger = initialize_logger()
    logger.debug("Performing validation of the GUFO data loaded from the YAML resource file...")

    # Verify if only the two necessary hierarchies were loaded.
    num_hierarchies = len(gufo_data.keys())
    if num_hierarchies != 2:
        logger.error(f"Data provided in YAML file is invalid: "
                     f"number of hierarchies different from the expected. Expected 2 but found {num_hierarchies}. "
                     f"Exiting program.")
        exit(1)

    # Verify if hierarchies were loaded.
    verify_loaded_hierarchy(gufo_data, "types")
    verify_loaded_hierarchy(gufo_data, "individuals")

    # Verify if the number of classes in the hierarchies are the expected number.
    verify_num_classes_hierarchy(gufo_data, "types")
    verify_num_classes_hierarchy(gufo_data, "individuals")

    # For each class in the hierarchies, verify if the sum of the items in its lists equals the expected number.
    verify_num_items_classes(gufo_data, "types")
    verify_num_items_classes(gufo_data, "individuals")

    # For each class in the hierarchies, there must be no duplicates (inside a list or between lists).
    verify_repeated_classes(gufo_data, "types")
    verify_repeated_classes(gufo_data, "individuals")

    # TODO (@pedropaulofb): Create new verification: every loaded element must be part of the expected list
    # Collect the expected list from the GUFO OWL file to be read?

    logger.debug("Validation of the GUFO data loaded from the YAML resource file successfully performed.")


def verify_loaded_hierarchy(gufo_data, hierarchy):
    """ Verify if the argument hierarchy was loaded. """

    logger = initialize_logger()

    if hierarchy not in gufo_data.keys():
        logger.error(f"Data provided in YAML resource file is invalid: "
                     f"{hierarchy.upper()} HIERARCHY not found. Exiting program.")
        exit(1)


def verify_num_classes_hierarchy(gufo_data, hierarchy):
    """ Verify if the number of classes in the argument hierarchy is the expected number. """
    logger = initialize_logger()

    number_classes = expected_number(hierarchy)

    length_types = len(gufo_data[hierarchy])
    if length_types != number_classes:
        logger.error(f"Data provided in YAML file is invalid: "
                     f"number of classes in the {hierarchy.upper()} HIERARCHY is different from the expected. "
                     f"Expected {number_classes} but found {length_types}. "
                     f"Exiting program.")
        exit(1)


def verify_num_items_classes(gufo_data, hierarchy):
    """ For each class in the argument hierarchy, verify if the sum of the items in its lists
    equals the expected number. """

    logger = initialize_logger()
    number_classes = expected_number(hierarchy)

    classes_list = list(gufo_data[hierarchy].keys())

    index = 0
    for it in classes_list:
        len_is_list = len(gufo_data[hierarchy][it]["is_list"])
        len_can_list = len(gufo_data[hierarchy][it]["can_list"])
        len_not_list = len(gufo_data[hierarchy][it]["not_list"])
        sum_len_lists = len_is_list + len_can_list + len_not_list
        if sum_len_lists != number_classes:
            logger.error(f"Data provided in YAML file is invalid: "
                         f"number of items in the {classes_list[index]} lists is different from the expected. "
                         f"Expected {number_classes} but found {sum_len_lists}. "
                         f"Exiting program.")
            exit(1)
        index += 1


def verify_repeated_classes(gufo_data, hierarchy):
    """ For each class in the argument hierarchy, there must be no duplicates (inside a list or between lists). """
    logger = initialize_logger()

    classes_list = list(gufo_data[hierarchy].keys())

    index = 0
    for it in classes_list:
        sum_list = gufo_data[hierarchy][it]["is_list"] \
                   + gufo_data[hierarchy][it]["can_list"] \
                   + gufo_data[hierarchy][it]["not_list"]
        if has_duplicates(sum_list):
            logger.error(f"Data provided in YAML file is invalid: "
                         f"Duplicated entry found in the lists for {classes_list[index]}. "
                         f"Exiting program.")
            exit(1)
        index += 1


def expected_number(hierarchy):
    """ Return the number of classes expected for the argument hierarchy. """

    logger = initialize_logger()
    NUMBER_CLASSES = 0

    if hierarchy == "types":
        NUMBER_CLASSES = NUMBER_CLASSES_TYPES
    elif hierarchy == "individuals":
        NUMBER_CLASSES = NUMBER_CLASSES_INDIVIDUALS
    else:
        logger.error(f"Invalid parameter when returning expected number for {hierarchy.upper()} HIERARCHY. "
                     f"Exiting program.")
        exit(1)

    return NUMBER_CLASSES
