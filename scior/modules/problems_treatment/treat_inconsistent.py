""" Functions related to the verification and treatment of identified INCONSISTENCY cases. """

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass

LOGGER = initialize_logger()


def report_inconsistency_case_in_rule(rule_code: str, ontology_dataclass: OntologyDataClass,
                                      additional_message: str = "") -> None:
    """ Reports inconsistency case detected and interrupts the software execution. """

    LOGGER.error(f"Inconsistency detected in rule {rule_code} for class {ontology_dataclass.uri}. "
                 f"{additional_message} Program aborted.")
    raise ValueError(f"Inconsistency found in rule.")


def report_inconsistency_case_in_dataclass(ontology_dataclass: OntologyDataClass, additional_message: str = "") -> None:
    """ Reports inconsistency detected when verifying ontology dataclasses and interrupts the software execution. """

    LOGGER.error(f"Inconsistency detected in {ontology_dataclass.uri}. "
                 f"{additional_message} Program aborted.")
    raise ValueError(f"Inconsistency found in ontology_dataclass consistency verification.")


def report_inconsistency_case_moving(ontology_dataclass: OntologyDataClass, additional_message: str = "") -> None:
    """ Reports inconsistency detected when moving a classification between ontology_dataclass' lists
        and interrupts the software execution.
    """

    LOGGER.error(f"Inconsistency detected in {ontology_dataclass.uri}. "
                 f"{additional_message} Program aborted.")
    raise ValueError(f"Inconsistency found when moving classifications in an ontology_dataclass.")
