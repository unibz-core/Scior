""" Functions related to reporting and treatment of execution errors. """

from scior.modules.problems_treatment.incompleteness import LOGGER


def report_error_dataclass_not_found(searched_uri: str):
    """ Reports the error caused when an item is searched in the ontology_dataclass_list and is not found. """

    LOGGER.error(f"Unexpected situation. Searched URI {searched_uri} "
                 f"not found in ontology_dataclass_list. Program aborted.")

    raise ValueError(f"INVALID VALUE!")
