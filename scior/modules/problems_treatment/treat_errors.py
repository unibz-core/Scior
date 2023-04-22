""" Functions related to the verification and treatment of identified ERROR cases. """

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def report_error_dataclass_not_found(searched_uri: str) -> None:
    """ Reports the error caused when an item is searched in the ontology_dataclass_list and is not found. """

    LOGGER.error(f"Unexpected situation. Searched URI {searched_uri} "
                 f"not found in ontology_dataclass_list. Program aborted.")
    raise ValueError(f"Searched OntologyDataClass not found!")


def report_error_end_of_switch(invalid_parameter: str) -> None:
    """ Reports the error caused when an invalid parameter is provided to a switch case (if-else statements). """

    LOGGER.error(f"Unexpected parameter received: {invalid_parameter}. Program aborted.")
    raise ValueError(f"End of switch (if-else statements) without valid parameter!")

# TODO (@pedropaulofb): Exceptions must have the following format:
# try:
#     result = 1/0
# except Exception as error:
#     logger.error(f"{error = }")
#     raise ValueError(error)
