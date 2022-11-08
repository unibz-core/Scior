""" Provides class and functions to calculate statistics of the improvement OntCatOWL has caused on
the inputted ontology. """

from modules.logger_config import initialize_logger

# These values must be updated for newer versions of OntCatOWL, after including elements other than Endurants.
NUMBER_GUFO_TYPES = 14
NUMBER_GUFO_INDIVIDUALS = 13


class dataclass_statistics(object):
    """ Class that contains the statistics for a single dataclass. """

    def __init__(self, ontology_dataclass):
        self.uri = ontology_dataclass.uri

        self.number_unknown_types = len(ontology_dataclass.can_type)
        self.number_unknown_individuals = len(ontology_dataclass.can_individual)

        self.number_known_types = len(ontology_dataclass.is_type) + len(ontology_dataclass.not_type)
        self.number_known_individuals = len(ontology_dataclass.is_individual) + len(ontology_dataclass.not_individual)


class list_classes_by_situation(object):
    """ Class that contains the uri of all classes in a specific situation.

    Situation field admitted values: "Totally Unknown", "Partially Known", "Totally Known".
    """

    def __init__(self, situation, list_uris_types, list_uris_individuals, list_uris_all):

        logger = initialize_logger()
        if situation == "Totally Unknown" or situation == "Partially Known" or situation == "Totally Known":
            self.situation = situation
            self.list_uris_types = list_uris_types
            self.list_uris_individuals = list_uris_individuals
            self.list_uris_all = list_uris_all
        else:
            logger.error("Unknown situation informed to list_classes_by_situation. Program aborted.")
            exit(1)


def generates_partial_statistics_list(ontology_dataclass_list):
    """ Collects the statistics of an ontology_dataclass_list.
    Returns a list of instances of the dataclass_statistics class.
    """

    partial_statistics_list = []

    for ontology_dataclass in ontology_dataclass_list:
        partial_statistics_list.append(dataclass_statistics(ontology_dataclass))

    return partial_statistics_list


def get_values_statistics(statistics_list):
    """ Receives a statistics list and returns two lists:
        list for classes: aggregated statistics for classes
        list for classifications: aggregated statistics for possible classifications (stereotypes) of classes

        FOR NUMBERS OF CLASSES:
            return_list_classes[0] = total_classes_number

            return_list_classes[1] = totally_unknown_classes_types
            return_list_classes[2] = totally_unknown_classes_individuals
            return_list_classes[3] = totally_unknown_classes_all

            return_list_classes[4] = partially_known_classes_types
            return_list_classes[5] = partially_known_classes_individuals
            return_list_classes[6] = partially_known_classes_all

            return_list_classes[7] = totally_known_classes_types
            return_list_classes[8] = totally_known_classes_individuals
            return_list_classes[9] = totally_known_classes_all

        FOR NUMBERS OF CLASSIFICATIONS:
            return_list_classifications[0] = total_classifications_number

            return_list_classifications[1] = total_classifications_types
            return_list_classifications[2] = total_classifications_individuals

            return_list_classifications[3] = number_unknown_classifications_types
            return_list_classifications[4] = number_known_classifications_types

            return_list_classifications[5] = number_unknown_classifications_individuals
            return_list_classifications[6] = number_known_classifications_individuals

            return_list_classifications[7] = number_unknown_classifications_total
            return_list_classifications[8] = number_known_classifications_total

            return_list_classifications[9] = 0 (empty)
    """
    logger = initialize_logger()

    # INITIALIZATION OF VARIABLES
    return_list_classes = []
    return_list_classifications = []
    total_classes_number = 0
    totally_unknown_classes_types = 0
    totally_unknown_classes_individuals = 0
    totally_unknown_classes_all = 0
    totally_known_classes_types = 0
    totally_known_classes_individuals = 0
    totally_known_classes_all = 0
    partially_known_classes_types = 0
    partially_known_classes_individuals = 0
    partially_known_classes_all = 0

    number_unknown_classifications_types = 0
    number_unknown_classifications_individuals = 0
    number_known_classifications_types = 0
    number_known_classifications_individuals = 0
    number_unknown_classifications_total = 0
    number_known_classifications_total = 0

    # CALCULATION OF VALUES
    for element in statistics_list:

        total_classes_number += 1

        # Calculating number of classifications for TYPES
        number_unknown_classifications_types += element.number_unknown_types
        number_known_classifications_types += element.number_known_types

        # Calculating number of classifications for INDIVIDUALS
        number_unknown_classifications_individuals += element.number_unknown_individuals
        number_known_classifications_individuals += element.number_known_individuals

        # Calculating number of classes for TYPES

        is_totally_unknown_classes_types = False
        is_totally_known_classes_types = False

        if element.number_unknown_types == NUMBER_GUFO_TYPES:
            totally_unknown_classes_types += 1
            is_totally_unknown_classes_types = True
        elif element.number_unknown_types == 0:
            totally_known_classes_types += 1
            is_totally_known_classes_types = True
        else:
            partially_known_classes_types += 1

        # Calculating number of classes for INDIVIDUALS

        is_totally_unknown_classes_individuals = False
        is_totally_known_classes_individuals = False

        if element.number_unknown_individuals == NUMBER_GUFO_INDIVIDUALS:
            totally_unknown_classes_individuals += 1
            is_totally_unknown_classes_individuals = True
        elif element.number_unknown_individuals == 0:
            totally_known_classes_individuals += 1
            is_totally_known_classes_individuals = True
        else:
            partially_known_classes_individuals += 1

        # Calculating number of classes for ALL

        if is_totally_known_classes_types and is_totally_known_classes_individuals:
            totally_known_classes_all += 1
        elif is_totally_unknown_classes_types and is_totally_unknown_classes_individuals:
            totally_unknown_classes_all += 1
        else:
            partially_known_classes_all += 1

    # Calculating number of classifications for TOTAL
    number_unknown_classifications_total += number_unknown_classifications_types + number_unknown_classifications_individuals
    number_known_classifications_total += number_known_classifications_types + number_known_classifications_individuals

    # GENERATING RETURN LISTS

    # Generating lists of numbers for classes
    return_list_classes.append(total_classes_number)

    return_list_classes.append(totally_unknown_classes_types)
    return_list_classes.append(totally_unknown_classes_individuals)
    return_list_classes.append(totally_unknown_classes_all)

    return_list_classes.append(partially_known_classes_types)
    return_list_classes.append(partially_known_classes_individuals)
    return_list_classes.append(partially_known_classes_all)

    return_list_classes.append(totally_known_classes_types)
    return_list_classes.append(totally_known_classes_individuals)
    return_list_classes.append(totally_known_classes_all)

    # Generating lists of numbers for classifications
    total_classifications_number = number_unknown_classifications_total + number_known_classifications_total
    total_classifications_types = number_unknown_classifications_types + number_known_classifications_types
    total_classifications_individuals = number_unknown_classifications_individuals + number_known_classifications_individuals

    return_list_classifications.append(total_classifications_number)

    return_list_classifications.append(total_classifications_types)
    return_list_classifications.append(total_classifications_individuals)

    return_list_classifications.append(number_unknown_classifications_types)
    return_list_classifications.append(number_known_classifications_types)

    return_list_classifications.append(number_unknown_classifications_individuals)
    return_list_classifications.append(number_known_classifications_individuals)

    return_list_classifications.append(number_unknown_classifications_total)
    return_list_classifications.append(number_known_classifications_total)

    return_list_classifications.append(0)

    if (
            totally_unknown_classes_types + partially_known_classes_types + totally_known_classes_types) != total_classes_number:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Totally Unknown. "
                     "Program aborted.")
        exit(1)
    if (
            totally_unknown_classes_individuals + partially_known_classes_individuals + totally_known_classes_individuals) != total_classes_number:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Partially Known. "
                     "Program aborted.")
        exit(1)
    if (totally_unknown_classes_all + partially_known_classes_all + totally_known_classes_all) != total_classes_number:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Totally Known. "
                     "Program aborted.")
        exit(1)

    return return_list_classes, return_list_classifications


def calculate_final_statistics(before_statistics, after_statistics):
    """ Receives 'before' and 'after' statistic lists and calculates final statistics.
    The 'before' and 'after' statistic lists are lists of statistics of all classes. I.e., it contains instances of
    the class dataclass_statistics.
    """

    list_classes_values_before, list_classifications_values_before = get_values_statistics(before_statistics)
    list_classes_values_after, list_classifications_values_after = get_values_statistics(after_statistics)

    # aggregated_classes_list_values [0:9] - before values
    # aggregated_classes_list_values [10:19] - after values

    aggregated_classes_list_values = list_classes_values_before + list_classes_values_after

    # aggregated_classifications_list_values [0:9] - before values
    # aggregated_classifications_list_values [10:19] - after values

    aggregated_classifications_list_values = list_classifications_values_before + list_classifications_values_after

    return aggregated_classes_list_values, aggregated_classifications_list_values


def get_list_totally_unknown_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in an list_classes_by_situation class.
        All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_totally_unknown_classes ...")

    list_classes_totally_unknown_types = []
    list_classes_totally_unknown_individuals = []
    list_classes_totally_unknown_all = []

    for element in class_statistics_list:
        if element.number_known_types == 0:
            list_classes_totally_unknown_types.append(element.uri)
        if element.number_known_individuals == 0:
            list_classes_totally_unknown_individuals.append(element.uri)
        if element.number_known_types + element.number_known_individuals == 0:
            list_classes_totally_unknown_all.append(element.uri)

    list_classes_totally_unknown_types.sort()
    list_classes_totally_unknown_individuals.sort()
    list_classes_totally_unknown_all.sort()

    list_totally_unknown_classes = list_classes_by_situation("Totally Unknown", list_classes_totally_unknown_types,
                                                             list_classes_totally_unknown_individuals,
                                                             list_classes_totally_unknown_all)

    logger.debug("list_totally_unknown_classes successfully generated.")

    return list_totally_unknown_classes


def get_list_partially_known_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in an list_classes_by_situation class.
        All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_partially_known_classes ...")

    list_classes_partially_known_types = []
    list_classes_partially_known_individuals = []
    list_classes_partially_known_all = []

    for element in class_statistics_list:
        if element.number_unknown_types != 0 and element.number_known_types != 0:
            list_classes_partially_known_types.append(element.uri)
        if element.number_unknown_individuals != 0 and element.number_known_individuals != 0:
            list_classes_partially_known_individuals.append(element.uri)
        if (element.number_unknown_types != 0 and element.number_known_types != 0) or (
                element.number_unknown_individuals != 0 and element.number_known_individuals != 0):
            list_classes_partially_known_all.append(element.uri)

    list_classes_partially_known_types.sort()
    list_classes_partially_known_individuals.sort()
    list_classes_partially_known_all.sort()

    list_partially_known_classes = list_classes_by_situation("Partially Known", list_classes_partially_known_types,
                                                             list_classes_partially_known_individuals,
                                                             list_classes_partially_known_all)

    logger.debug("list_partially_known_classes successfully generated.")

    return list_partially_known_classes


def get_list_totally_known_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in an list_classes_by_situation class.
    All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_totally_known_classes ...")

    list_classes_totally_known_types = []
    list_classes_totally_known_individuals = []
    list_classes_totally_known_all = []

    for element in class_statistics_list:
        if element.number_unknown_types == 0:
            list_classes_totally_known_types.append(element.uri)
        if element.number_unknown_individuals == 0:
            list_classes_totally_known_individuals.append(element.uri)
        if element.number_unknown_types + element.number_unknown_individuals == 0:
            list_classes_totally_known_all.append(element.uri)

    list_classes_totally_known_types.sort()
    list_classes_totally_known_individuals.sort()
    list_classes_totally_known_all.sort()

    list_totally_known_classes = list_classes_by_situation("Totally Known", list_classes_totally_known_types,
                                                           list_classes_totally_known_individuals,
                                                           list_classes_totally_known_all)

    logger.debug("list_totally_known_classes successfully generated.")

    return list_totally_known_classes


def generate_result_classes_lists(before_statistics, after_statistics):
    """ Receives 'before' and 'after' statistics and generates lists of improved and solved classes."""

    lists_before = []
    lists_after = []

    # Getting lists with classes names
    list_totally_unknown_classes_before = get_list_totally_unknown_classes(before_statistics)
    list_partially_known_classes_before = get_list_partially_known_classes(before_statistics)
    list_totally_known_classes_before = get_list_totally_known_classes(before_statistics)

    list_totally_unknown_classes_after = get_list_totally_unknown_classes(after_statistics)
    list_partially_known_classes_after = get_list_partially_known_classes(after_statistics)
    list_totally_known_classes_after = get_list_totally_known_classes(after_statistics)

    lists_before.append("Before")
    lists_before.append(list_totally_unknown_classes_before)
    lists_before.append(list_partially_known_classes_before)
    lists_before.append(list_totally_known_classes_before)

    lists_after.append("After")
    lists_after.append(list_totally_unknown_classes_after)
    lists_after.append(list_partially_known_classes_after)
    lists_after.append(list_totally_known_classes_after)

    return lists_before, lists_after
