""" Functions related to the verification and treatment of problems_treatment and inconsistency cases. """
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


class IncompletenessEntry(object):
    """ Class to store information about incompleteness identified during the software execution to be
        later reported to the user. Its attributes are:

        rule_code: str - Rule that detected the incompleteness case.
        list_affected_ontology_dataclasses_uris: list[str] - All classes affected by the detected incompleteness.
        message: str - Additional message to be reported together with the incompleteness case.
    """

    def __init__(self, entry_id: int, rule_code: str, list_affected_ontology_dataclasses_uris: list[str],
                 incompleteness_message: str = ""):
        self.entry_id = entry_id
        self.rule_code = rule_code
        self.list_affected_ontology_dataclasses_uris = list_affected_ontology_dataclasses_uris
        self.incompleteness_message = incompleteness_message


def add_to_incompleteness_stack(incompleteness_stack: list[IncompletenessEntry], rule_code: str,
                                list_affected_ontology_dataclasses_uris: list[str],
                                incompleteness_message: str = "") -> None:
    """ Adds a new entry to the incompleteness stack (received as parameter).

        The entry is composed of:
        (i) rule code,
        (ii) a list with URIs of all classes affected by detected incompleteness,
        (iii) and a message to be reported to the user.
    """

    new_entry = IncompletenessEntry(entry_id=len(incompleteness_stack) + 1, rule_code=rule_code,
                                    list_affected_ontology_dataclasses_uris=list_affected_ontology_dataclasses_uris,
                                    incompleteness_message=incompleteness_message)

    incompleteness_stack.append(new_entry)


def incompleteness_already_registered(rule_code: str, ontology_dataclass) -> bool:
    """ Verifies if a problems_treatment case has already being registered/reported for the received ontology_dataclass.

        Returns True if the problems_treatment for a specific rule has already been registered/reported.
        Returns False otherwise.
    """

    if ontology_dataclass.is_incomplete["is_incomplete"] and (
            rule_code in ontology_dataclass.is_incomplete["detected_in"]):
        return True
    else:
        return False


def register_incompleteness(rule_code: str, ontology_dataclass, additional_message: str = ""):
    """ Registers the ontology_dataclass incompleteness_info field and insert the rule in the detected_in list. """

    if not incompleteness_already_registered(rule_code, ontology_dataclass):
        LOGGER.warning(f"Rule {rule_code}: Incompleteness detected for class {ontology_dataclass.uri}. "
                       f"{additional_message}")
        ontology_dataclass.is_incomplete["is_incomplete"] = True
        ontology_dataclass.is_incomplete["detected_in"].append(rule_code)
