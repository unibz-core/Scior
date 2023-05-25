""" Auxiliary functions used for testing Scior. """
import csv

from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.utils_dataclass import get_dataclass_by_uri


def get_test_list() -> list[tuple]:
    """ Loads information about test test_files from csv and creates a list of tuples with tests' information.

    :return: The returned tuples' content is:
                row[0] (str) input file name: name of the input file to be tested using Scior.
                row[1] (str) output file name: file with the expected output to be compared with Scior's results.
                row[2] (str) world-assumption to be used in the test. Can assume the values "cwa", "owa", or "owaf".
                row[3] (bool) expected consistency: indicates if the result is expected to be consistent or not.
                row[4] (bool) expected result: indicates if the result is expected to be correct or not.
    :rtype: list[tuple]
    """

    tests_information = []

    with open('./test_files/all_tests.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            single_test = tuple(row.values())
            tests_information.append(single_test)

    return tests_information


def validate_results(input_list: list[OntologyDataClass], output_list: list[OntologyDataClass]) -> bool:
    """ Receives the input list of dataclasses and the output list and checks if all classifications from the
    output list classes are in the correspondent input list classes.

    :param input_list: List of classes obtained from input file with classifications after Scior's execution.
    :type input_list: list[OntologyDataClass]
    :param output_list: List of classes obtained from output file with expected classifications for each class.
    :type output_list: list[OntologyDataClass]
    :return: Indicates if all expected classifications were obtained (True) or not (False).
    :rtype: bool
    """

    result_correct = True

    for out_class in output_list:
        in_class = get_dataclass_by_uri(input_list, out_class.uri)

        if not set(out_class.is_type).issubset(set(in_class.is_type)) or not set(out_class.not_type).issubset(
                set(in_class.not_type)):
            result_correct = False
            break

    return result_correct
