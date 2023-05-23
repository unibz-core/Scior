""" Auxiliary functions used for testing Scior. """
import csv


def create_tests_lists() -> list[tuple]:
    """ Loads information about test files from csv and creates a list of tuples with tests' information.

    The returned tuples' content is:

    1. (str) input file name: name of the input file to be tested.
    2. (str) output file name: file with the expected output to be compared with Scior's results.
    3. (bool) result cwa: indicates if the result is expected to be consistent or not when performed in CWA.
    4. (bool) result owa: indicates if the result is expected to be consistent or not when performed in OWA.
    5. (bool) result owaf: indicates if the result is expected to be consistent or not when performed in OWAf.

    :return: Three tuples for tests, in the following order: CWA, OWA, and OWAf. Each one has the following format:
    [(str) input file name, (str) output file name, (bool) result cwa, (bool) result owa, (bool) result owaf].
    :rtype: tuple[tuple, tuple, tuple]
    """

    print("is here 0")

    with open('./files/all_tests.csv', mode='r') as csv_file:
        print("is here 1")
        csv_reader = csv.DictReader(csv_file)
        data_as_list = list(csv_reader)
        print("is here 2")
        print(data_as_list)

    all_tests = []

    return all_tests
