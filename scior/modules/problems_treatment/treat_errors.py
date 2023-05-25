""" Functions related to the verification and treatment of identified ERROR cases. """
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def report_error_requirement_not_met(error_message: str) -> None:
    """ Reports the error caused when a Scior requirement is not met. As this is a generic function, the error message
    parameter must be used to identify the error to the user.

    :param error_message: Message to be printed to the user indicating the detected error.
    :type error_message: str
    """

    LOGGER.error(f"{error_message} Program aborted.")
    raise ValueError(f"Scior's requirement not met!")


def report_error_dataclass_not_found(searched_uri: str) -> None:
    """ Reports the error caused when an item is searched in the ontology_dataclass_list and is not found.

    :param searched_uri: URI of the class that caused the error (i.e., that was searched and not found).
    :type searched_uri: str
    """

    LOGGER.error(f"Unexpected situation. Searched URI {searched_uri} "
                 f"not found in ontology_dataclass_list. Program aborted.")
    raise ValueError(f"Searched OntologyDataClass not found!")


def report_error_end_of_switch(invalid_parameter: str, caller_function_name: str) -> None:
    """ Reports the error caused when an invalid parameter is provided to a switch case (if-else statements).

    NOTE: caller_function_name can be obtained from 'current_function = inspect.stack()[0][3]'

    :param invalid_parameter: Invalid function parameter that caused the error.
    :type invalid_parameter: str
    :param caller_function_name: Name of the function in which the invalid parameter was used.
    :type caller_function_name: str
    """

    LOGGER.error(f"Unexpected parameter {invalid_parameter} received in function {caller_function_name}. "
                 f"Program aborted.")
    raise ValueError(f"End of switch (if-else statements) without valid parameter!")


def report_error_io_read(desired_content: str, file_description: str, error: OSError) -> None:
    """ Reports the error caused program cannot read or load the desired content (test_files or directories).

    :param desired_content: Name of the file used by the IO operation caused the error.
    :type desired_content: str
    :param file_description: Description of the file in desired_content.
    :type file_description: str
    :param error: Error raised by the IO operation.
    :type error: OSError
    """

    LOGGER.error(f"Could not load or read the {file_description} {desired_content}. Program aborted.")
    raise OSError(error)


def report_error_io_write(desired_content: str, file_description: str, error: OSError) -> None:
    """ Reports the error caused program cannot save or write the desired content (test_files or directories).

    :param desired_content: Name of the file used by the IO operation caused the error.
    :type desired_content: str
    :param file_description: Description of the file in desired_content.
    :type file_description: str
    :param error: Error raised by the IO operation.
    :type error: OSError
    """

    LOGGER.error(f"Could not create, write, or save the {file_description} {desired_content}. Program aborted.")
    raise OSError(error)
