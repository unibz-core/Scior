""" Functions related to the verification and treatment of incompleteness and inconsistency cases. """
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def report_error_dataclass_not_found(searched_uri: str):
    """ Reports the error caused when an item is searched in the ontology_dataclass_list and is not found. """

    LOGGER.error(f"Unexpected situation. Searched URI {searched_uri} "
                 f"not found in ontology_dataclass_list. Program aborted.")

    raise ValueError(f"INVALID VALUE!")


def incompleteness_already_registered(rule_code: str, ontology_dataclass) -> bool:
    """ Verifies if an incompleteness case has already being registered/reported for the received ontology_dataclass.

        Returns True if the incompleteness for a specific rule has already been registered/reported.
        Returns False otherwise.
    """

    if ontology_dataclass.incompleteness_info["is_incomplete"] and (
            rule_code in ontology_dataclass.incompleteness_info["detected_in"]):
        return True
    else:
        return False


def register_incompleteness(rule_code: str, ontology_dataclass, additional_message: str = ""):
    """ Registers the ontology_dataclass incompleteness_info field and insert the rule in the detected_in list. """

    if not incompleteness_already_registered(rule_code, ontology_dataclass):
        LOGGER.warning(f"Rule {rule_code}: Incompleteness detected for class {ontology_dataclass.uri}. "
                       f"{additional_message}")
        ontology_dataclass.incompleteness_info["is_incomplete"] = True
        ontology_dataclass.incompleteness_info["detected_in"].append(rule_code)
