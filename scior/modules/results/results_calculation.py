""" Functions related to aquisition, calculation, generation, and other activities related to the final statistics. """
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.results.results_data import ResultsInformationClass


def collect_results_information(results_information: ResultsInformationClass,
                                ontology_dataclass_list: list[OntologyDataClass], situation: str):
    """ Collect data from dataclass_list and populate the results_information. """

    # TODO (@pedropaulofb): TREAT COLLECT CLASSIFICATIONS

    for ontology_dataclass in ontology_dataclass_list:

        is_size = len(ontology_dataclass.is_type)
        not_size = len(ontology_dataclass.not_type)

        # Collecting TOTALLY UNKNOWN
        if is_size + not_size == 0:
            if situation == "before":
                results_information.tu_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.tu_list_a.append(ontology_dataclass.uri)
            # else:
                # TODO (@pedropaulofb): Implement REPORT ERROR

        # Collecting TOTALLY KNOWN
        elif len(ontology_dataclass.can_type) == 0:
            if situation == "before":
                results_information.tk_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.tk_list_a.append(ontology_dataclass.uri)
            # else:
                # TODO (@pedropaulofb): Implement REPORT ERROR

        # Collecting PARTIALLY KNOWN
        else:
            if situation == "before":
                results_information.pk_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.pk_list_a.append(ontology_dataclass.uri)
            # else:
                # TODO (@pedropaulofb): Implement REPORT ERROR


def generate_results_information(before_dataclass_list: list[OntologyDataClass],
                                 after_dataclass_list: list[OntologyDataClass]) -> ResultsInformationClass:
    """ Create statistics dictionary with all Scior execution' statistics. """

    # TODO (@pedropaulofb): Treat specific case that all unknown classes starts with 1 known classification.

    results_information = ResultsInformationClass()

    # Collecting BEFORE information for classes
    collect_results_information(results_information, before_dataclass_list, "before")
    collect_results_information(results_information, after_dataclass_list, "after")

    # Calculating derived information
    results_information.calculate_information()

    return results_information
