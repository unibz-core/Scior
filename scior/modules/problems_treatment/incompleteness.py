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


def include_incompleteness_and_keep_updated(new_incompleteness_entry: IncompletenessEntry,
                                            incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Verify if the new entry received as parameter:
            (i) can be directly included into the incompleteness stack or
            (ii) if it updates an old entry (that must be removed).
        Afer the verification the new entry is included into the incompleteness stack.
    """

    # Registering the new incompleteness entry into the incompleteness_stack
    incompleteness_stack.append(new_incompleteness_entry)


def register_incompleteness(incompleteness_stack: list[IncompletenessEntry], rule_code: str,
                            list_affected_ontology_dataclasses_uris: list[str], incompleteness_message: str,
                            arguments: dict) -> None:
    """ Adds a new entry to the incompleteness stack (received as parameter).

        Design rationale:   An ontology can be incomplete, not a class.
                            The ontology has classes affected by incompleteness cases.

        The entry is composed of:
            - an id,
            - a rule code,
            - a list with URIs of all classes affected by detected incompleteness, and
            - a message to be reported to the user.
    """

    # Sorting affected classes
    list_affected_ontology_dataclasses_uris.sort()

    # Creating new incompleteness entry
    new_entry = IncompletenessEntry(entry_id=len(incompleteness_stack) + 1, rule_code=rule_code,
                                    list_affected_ontology_dataclasses_uris=list_affected_ontology_dataclasses_uris,
                                    incompleteness_message=incompleteness_message)

    include_incompleteness_and_keep_updated(new_entry, incompleteness_stack)


def print_all_incompleteness(incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Print all incompleteness at the end of the execution when authorized by the user using the arguments. """

    if arguments["verbosity2"]:
        for incompleteness_entry in incompleteness_stack:
            # Log incompleteness case to user if enabled by argument
            LOGGER.info(f"Rule {incompleteness_entry.rule_code}: New incompleteness found! "
                        f"Related classes {incompleteness_entry.list_affected_ontology_dataclasses_uris}. "
                        f"{incompleteness_entry.incompleteness_message}")

    pass
