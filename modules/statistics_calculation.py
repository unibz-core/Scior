""" Provides class and functions to calculate statistics of the improvement OntCatOWL has caused on
the inputted ontology. """

# These values must be updated for newer versions of OntCatOWL, after including elements other than Endurants.
NUMBER_GUFO_TYPES = 14
NUMBER_GUFO_INDIVIDUALS = 13


class dataclass_statistics(object):
    """ Class that contains the statistics for a dataclasses. """

    def __init__(self, ontology_dataclass):
        self.uri = ontology_dataclass.uri

        self.number_unknown_types = len(ontology_dataclass.can_type)
        self.number_unknown_individuals = len(ontology_dataclass.can_individual)

        self.number_known_types = len(ontology_dataclass.is_type) + len(ontology_dataclass.not_type)
        self.number_known_individuals = len(ontology_dataclass.is_individual) + len(ontology_dataclass.not_individual)


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
        print("ERRO 1")
        exit(1)
    if (totally_unknown_individuals + partially_known_individuals + totally_known_individuals) != total_size:
        print("ERRO 2")
        exit(1)
    if (totally_unknown_all + partially_known_all + totally_known_all) != total_size:
        print("ERRO 3")
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
