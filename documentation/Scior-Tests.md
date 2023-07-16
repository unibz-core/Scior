# Scior: Tests

Scior relies on [Pytest](https://docs.pytest.org/en/7.4.x/) to perform its automated tests. Currently, over two hundred tests analyze Scior’s three world assumptions (OWA, CWA, and OWA-F).

This document will overview the testing process.

## Resources Locations

The following resources are available:

1.  Implementation code: <https://github.com/unibz-core/Scior/tree/main/tests>

2.  Fixture and individual test files: <https://github.com/unibz-core/Scior/tree/main/tests/test_files>

3.  List with tests in `.tsv` (tab-separated) format: https://github.com/unibz-core/Scior/blob/main/documentation/resources/scior_tests.tsv

## Automated Testing

A csv file is used to provide the [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) (used to feed input data to the tests) and then each line is tested.

### Test Inputs

#### Fixture format

Each line has the following information:

- `input_file` (string): Path to an owl file that is going to be used to test Scior.
- `output_file` (string): Path to an owl file that contains the expected results for the Scior execution.
- `assumption` (string): World-assumption to be used in the Scior test (a Scior’s execution argument).
- `is_consistent` (boolean): Indicates if the ontology is expected to be consistent or not.
- `is_correct` (boolean): Indicates if the generated result is expected to equal the provided output or not.

#### Test file format

The input file (the `intput_file` test argument) is the file to be processed by Scior to generate a result file. The result must not be mistaken as the output file (the `output_file` test argument). Scior's execution produces the former, which will be compared to the latter file to evaluate the test result. The output file’s content corresponds to the input file changed to include the information to be verified.

## Execution Process

Each csv line is an independent test. Each test is performed according to the flowchart below.

![test flowchart](https://raw.githubusercontent.com/unibz-core/Scior/main/documentation/resources/images/Test%20Flowchart.png)

At the start, Scior receives the input owl file to be processed and the execution mode (world assumption) in which it must operate.

During execution, inconsistencies are compared to expected consistency provided as fixture. If `is_consistent` is 'False' (showing that the input model was already expected to be inconsistent), the test result is positive. If the outcome was expected to be consistent (`is_consistency` fixture set to 'True'), then the test will have a negative result.

Otherwise, if Scior concludes its processing without detect an inconsistency, then the same verification will be done regarding the expected consistency. If the expected consistency was set as 'True', it matched the one got and then a second evaluation will be performed.

The second evaluation regards the comparison of the produced result and the output provided to the test as fixture. Their comparison is going to be checked over the information about if it was expected to happen or not (`is_correct` fixture set to 'True' or 'False', respectively). If the result and output were equal and that was the expected situation (`is_correct` is 'True'), then the test will be positive. If they do not match, but that was the expected situation (`is_correct` is 'False'), then the test will also be positive.
