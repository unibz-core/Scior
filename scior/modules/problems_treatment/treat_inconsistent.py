""" Functions related to the verification and treatment of identified INCONSISTENCY cases. """
from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def report_inconsistency_case_in_rule(rule_code: str, ontology_dataclass: OntologyDataClass,
                                      additional_message: str = "") -> None:
    """ Reports inconsistency case detected and interrupts the software execution. """

    LOGGER.error(f"Inconsistency detected in rule {rule_code} for class {ontology_dataclass.uri}. "
                 f"{additional_message} Program aborted.")
    raise ValueError(f"Inconsistency found in rule.")
