""" Functions related to aquisition, calculation, generation, and other activities related to the final statistics. """
import inspect

from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry
from scior.modules.results.results_data import ResultsInformationClass


def collect_incompleteness_information(results_information: ResultsInformationClass,
                                       incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Populate information about incompleteness cases in the results_information class. """

    list_incompleteness_rules = []

    for incompleteness_case in incompleteness_stack:
        list_incompleteness_rules.append(incompleteness_case.rule_code)

    # Setting number of uncompleteness cases
    results_information.num_incompleteness = len(list_incompleteness_rules)

    # Creating dictionary and collecting information
    temp_dict = dict()
    for i in list_incompleteness_rules:
        temp_dict[i] = temp_dict.get(i, 0) + 1

    # Sorting and asserting to results_information object
    temp_dict_keys = list(temp_dict.keys())
    temp_dict_keys.sort()
    results_information.incompleteness_dict = {i: temp_dict[i] for i in temp_dict_keys}


def collect_results_information(results_information: ResultsInformationClass,
                                ontology_dataclass_list: list[OntologyDataClass], situation: str):
    """ Collect classes and classifications data from dataclass_list and populate the results_information.

        Note: is_size receives -1 because the dataclasses already start with the base classification as known.
        Hence, this information must be subtracted to generated valid results. As instance, when having EndurantType
        as base gUFO classification, if not treated a class 'X' would already start classified as a partially
        known class, what is invalid.
    """

    current_function = inspect.stack()[0][3]

    for ontology_dataclass in ontology_dataclass_list:

        is_size = len(ontology_dataclass.is_type) - 1
        can_size = len(ontology_dataclass.can_type)
        not_size = len(ontology_dataclass.not_type)

        # CLASSES: Collecting TOTALLY UNKNOWN
        # The verification number is one because of the base classification (for now, EndurantType)
        if is_size + not_size == 0:
            if situation == "before":
                results_information.tu_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.tu_list_a.append(ontology_dataclass.uri)
            else:
                report_error_end_of_switch(situation, current_function)

        # CLASSES: Collecting TOTALLY KNOWN
        elif len(ontology_dataclass.can_type) == 0:
            if situation == "before":
                results_information.tk_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.tk_list_a.append(ontology_dataclass.uri)
            else:
                report_error_end_of_switch(situation, current_function)

        # CLASSES: Collecting PARTIALLY KNOWN
        else:
            if situation == "before":
                results_information.pk_list_b.append(ontology_dataclass.uri)
            elif situation == "after":
                results_information.pk_list_a.append(ontology_dataclass.uri)
            else:
                report_error_end_of_switch(situation, current_function)

        # Collecting CLASSIFICATIONS
        if situation == "before":
            results_information.num_uc_b += can_size
            results_information.num_kc_b += (is_size + not_size)
        elif situation == "after":
            results_information.num_uc_a += can_size
            results_information.num_kc_a += (is_size + not_size)
        else:
            report_error_end_of_switch(situation, current_function)


def generate_results_information(before_dataclass_list: list[OntologyDataClass],
                                 after_dataclass_list: list[OntologyDataClass],
                                 incompleteness_stack: list[IncompletenessEntry]) -> ResultsInformationClass:
    """ Create statistics dictionary with all Scior execution' statistics. """

    # Creating object for storing the results information
    results_information = ResultsInformationClass()

    # Collecting before and after results data
    collect_results_information(results_information, before_dataclass_list, "before")
    collect_results_information(results_information, after_dataclass_list, "after")

    # Calculating derived information
    results_information.calculate_information()

    # Collecting information about incompleteness cases found
    collect_incompleteness_information(results_information, incompleteness_stack)

    return results_information
