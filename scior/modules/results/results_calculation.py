""" Functions related to aquisition, calculation, generation, and other activities related to the final statistics. """
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.results.results_data import results_statistics_class


def calculate_numbers_classes(before_dataclass_list: list[OntologyDataClass],
                                 after_dataclass_list: list[OntologyDataClass]) -> dict:

    # Initial number of totally unknown classes
    # Final number of totally unknown classes

    for before_dataclass in before_dataclass_list:
        if len(before_dataclass.is_type):
            results_statistics["TU_before"]+= 1

    print(results_statistics)
    exit(3)

    # Initial number of partially known classes
    # Final number of partially known classes

    # Initial number of totally known classes
    # Final number of totally known classes

    return results_statistics


def calculate_numbers_classifications():
    # sum unknown (can_type) before
    # sum known (is_type + not_type) before

    # sum unknown (can_type) after
    # sum known (is_type + not_type) after

    pass


def generate_lists():
    # List of totally unknown classes before
    # List of totally unknown classes after

    # List of partially known classes before
    # List of partially known classes after

    # List of totally known classes before
    # List of totally known classes after

    pass


def calculate_percentages_classes():
    # percentage totally unknown after/before
    # percentage partially known after/before
    # percentage totally known after/before

    pass


def calculate_percentages_classifications():
    pass


def calculate_results_statistics(before_dataclass_list: list[OntologyDataClass],
                                 after_dataclass_list: list[OntologyDataClass]) -> dict:
    """ Create statistics dictionary with all Scior execution' statistics. """

    results_statistics = results_statistics_class()

    # Initial number of totally unknown classes
    # Final number of totally unknown classes

    for before_dataclass in before_dataclass_list:
        if len(before_dataclass.is_type):
            results_statistics["TU_before"] += 1

    print(results_statistics)
    exit(3)

    return results_statistics