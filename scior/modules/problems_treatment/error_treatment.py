""" Functions related to reporting and treatment of execution errors. """
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def report_error_dataclass_not_found(searched_uri: str):
    """ Reports the error caused when an item is searched in the ontology_dataclass_list and is not found. """

    LOGGER.error(f"Unexpected situation. Searched URI {searched_uri} "
                 f"not found in ontology_dataclass_list. Program aborted.")

    raise ValueError(f"INVALID VALUE!")





    # TODO (@pedropaulofb): Exceptions must have the following format:
    # try:
    #     result = 1/0
    # except Exception as error:
    #     logger.error(f"{error = }")
    #     raise ValueError(error)