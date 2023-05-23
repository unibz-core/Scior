""" Main file for executing Scior's tests. """
from scior.main import run_scior_test_execution


# 1. run single test for single assumption
# 2. run single test for multiple assumption
# 3. run multiple test for multiple assumption


def test_scior():

    input_file = "tests/files/test_ra01_in.ttl"
    output_file = "tests/files/test_ra01_out.ttl"
    expected_owa = True

    try:
        input_dataclass_list = run_scior_test_execution("input", input_file,"owa")
        output_dataclass_list = run_scior_test_execution("output", input_file,"owa")

        # If the test is expected to be valid and results are OK
        print("\tTEST OK")
        if expected_owa:
            assert True
        else:
            assert False

    except:
        print("\tTEST ERROR")

        # If the test is expected to be valid but is here, than NOT OK
        if expected_owa:
            assert False
        else:
            assert False

    # if assertion expected result TRUE:
        # execute scior on input file
        # create list for output_file
        # check if out_list matches scior results
    # if assertion expected result FALSE:
        # execute scior on input file
        # if raised exception, OK
        # else NOT OK


    assert True
