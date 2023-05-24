""" Main file for executing Scior's tests. """
import pytest

from scior.main import run_scior_test_execution
from scior.modules.problems_treatment.treat_inconsistent import InconsistentOntology
from tests.test_aux import validate_results, get_test_list

LIST_OF_TESTS = get_test_list()


@pytest.mark.parametrize("input_file, output_file, assumption, expected", LIST_OF_TESTS)
def test_scior(input_file: str, output_file: str, assumption: str, expected: str):
    """ Executes Scior in a received input file and checks if the execution result matches the expected value.

    :param input_file: Path to file that is going to be used to test Scior.
    :type input_file: str
    :param output_file: Path to a file that contains the expected results for the Scior execution.
    :type output_file: str
    :param assumption: World-assumption to be used in the Scior test.
    :type assumption: str
    :param expected: Indicates if the ontology is expected to be consistent or not.
    :type expected: str
    """

    # Default values
    base_path = "tests/files/"
    is_correct = True
    no_error = True
    is_consistent = True

    # Adjusting inputs
    input_file = base_path + input_file
    output_file = base_path + output_file
    expected = True if expected == "True" else False

    try:
        # Creating input and output dataclass_lists
        input_dataclass_list = run_scior_test_execution("input", input_file, assumption)
        output_dataclass_list = run_scior_test_execution("output", output_file, assumption)

        # Checking if values from output file (expected) are in the calculated results
        is_correct = validate_results(input_dataclass_list, output_dataclass_list)
        is_consistent = True

    except InconsistentOntology:
        is_consistent = False
    except Exception:
        no_error = False

    # Setting problem messages
    exp_result_msg = "consistent" if expected else "inconsistent"
    consistency_msg = "consistent" if is_consistent else "inconsistent"

    assert no_error, f"EXECUTION ERROR! Error not associated with file consistency or Scior's results."
    assert expected == is_consistent, f"CONSISTENCY NOT MATCHED! Expected {exp_result_msg}, got {consistency_msg}."
    assert is_correct, f"RESULTS NOT MATCHED! Expected output provided does not match processed input content."
