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

    Situation field admitted values: "totally unknown", "partially known", "totally known".
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
    """ Collects the statistics of an ontology_dataclass_list. """

    partial_statistics_list = []

    for ontology_dataclass in ontology_dataclass_list:
        partial_statistics_list.append(dataclass_statistics(ontology_dataclass))

    return partial_statistics_list


def get_values_statistics(statistics_list):
    """ Receives a statistics list and return basic values in a list.

        return_list[0] = total_size

        return_list[1] = totally_unknown_types
        return_list[2] = totally_unknown_individuals
        return_list[3] = totally_unknown_all

        return_list[4] = partially_known_types
        return_list[5] = partially_known_individuals
        return_list[6] = partially_known_all

        return_list[7] = totally_known_types
        return_list[8] = totally_known_individuals
        return_list[9] = totally_known_all
    """
    logger = initialize_logger()

    # Initialization of variables
    return_list = []
    total_size = 0
    totally_unknown_types = 0
    totally_unknown_individuals = 0
    totally_unknown_all = 0
    totally_known_types = 0
    totally_known_individuals = 0
    totally_known_all = 0
    partially_known_types = 0
    partially_known_individuals = 0
    partially_known_all = 0

    # Calculation of values 
    for element in statistics_list:

        total_size += 1

        # Calculating for TYPES

        is_totally_unknown_types = False
        is_totally_known_types = False

        if element.number_unknown_types == NUMBER_GUFO_TYPES:
            totally_unknown_types += 1
            is_totally_unknown_types = True
        elif element.number_unknown_types == 0:
            totally_known_types += 1
            is_totally_known_types = True
        else:
            partially_known_types += 1

        # Calculating for INDIVIDUALS

        is_totally_unknown_individuals = False
        is_totally_known_individuals = False

        if element.number_unknown_individuals == NUMBER_GUFO_INDIVIDUALS:
            totally_unknown_individuals += 1
            is_totally_unknown_individuals = True
        elif element.number_unknown_individuals == 0:
            totally_known_individuals += 1
            is_totally_known_individuals = True
        else:
            partially_known_individuals += 1

        # Calculating for ALL

        if is_totally_known_types and is_totally_known_individuals:
            totally_known_all += 1
        elif is_totally_unknown_types and is_totally_unknown_individuals:
            totally_unknown_all += 1
        else:
            partially_known_all += 1

    # Generating return list

    return_list.append(total_size)

    return_list.append(totally_unknown_types)
    return_list.append(totally_unknown_individuals)
    return_list.append(totally_unknown_all)

    return_list.append(partially_known_types)
    return_list.append(partially_known_individuals)
    return_list.append(partially_known_all)

    return_list.append(totally_known_types)
    return_list.append(totally_known_individuals)
    return_list.append(totally_known_all)

    if (totally_unknown_types + partially_known_types + totally_known_types) != total_size:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Totally Unknown. "
                     "Program aborted.")
        exit(1)
    if (totally_unknown_individuals + partially_known_individuals + totally_known_individuals) != total_size:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Partially Known. "
                     "Program aborted.")
        exit(1)
    if (totally_unknown_all + partially_known_all + totally_known_all) != total_size:
        logger.error("Sum of number of classes is incorrect when calculating statistics - Totally Known. "
                     "Program aborted.")
        exit(1)

    return return_list


def calculate_final_statistics(before_statistics, after_statistics):
    """ Receives 'before' and 'after' statistics and calculates final statistics."""

    list_values_before = get_values_statistics(before_statistics)
    list_values_after = get_values_statistics(after_statistics)

    aggregated_list_values = list_values_before + list_values_after

    # aggregated_list_values [0:9] - before values
    # aggregated_list_values [10:19] - after values

    return aggregated_list_values


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
