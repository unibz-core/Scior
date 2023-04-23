""" Functions related to the verification and treatment of identified INCOMPLETENESS cases. """
import random
import string

from scior.modules.dataclass_definitions_ontology import OntologyDataClass

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


class IncompletenessEntry(object):
    """ Class to store information about incompleteness identified during the software execution to be
        later reported to the user. Its attributes are:

        rule_code: str - Rule that detected the incompleteness case.
        affected_dataclass_uri: str - URI of the classes affected by the detected incompleteness.
        message: str - Additional message to be reported together with the incompleteness case.
    """

    def __init__(self, entry_id: str, rule_code: str, affected_dataclass_uri: str,
                 incompleteness_message: str = ""):
        self.entry_id = entry_id
        self.rule_code = rule_code
        self.affected_dataclass_uri = affected_dataclass_uri
        self.incompleteness_message = incompleteness_message


def include_incompleteness_and_keep_updated(new_entry: IncompletenessEntry,
                                            incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Verify if the new entry received as parameter:
            (i) can be directly included into the incompleteness stack or
            (ii) if it updates an old entry (that must be removed).

        After the verification the new entry is included into the incompleteness stack and, if necessary,
        the old (outdated) entry is removed.

        AUXILIARY FUNCTION ONLY! MUST NOT BE USED OUTSIDE FUNCTION register_incompleteness.
    """

    # If new entry's rule and list of affected classes are already in the incompleteness stack, remove the old entry.
    for registered_entry in incompleteness_stack:
        if (registered_entry.rule_code == new_entry.rule_code) and (
                registered_entry.affected_dataclass_uri == new_entry.affected_dataclass_uri):
            LOGGER.debug(f"Outdated incompleteness entry (entry_id: {registered_entry.entry_id}) "
                         f"substituted for an updated one (entry_id: {new_entry.entry_id}).")
            incompleteness_stack.remove(registered_entry)

    # Registering the new incompleteness entry into the incompleteness_stack
    incompleteness_stack.append(new_entry)


def register_incompleteness(incompleteness_stack: list[IncompletenessEntry], rule_code: str,
                            affected_ontology_dataclass: OntologyDataClass, incompleteness_message: str) -> None:
    """ Adds a new entry to the incompleteness stack (received as parameter).

        The entry is composed of:
            - an id,
            - a rule code,
            - a list with the URI of the classe affected by the detected incompleteness, and
            - a message to be reported to the user.
    """

    new_entry_id = ''.join(random.choices(string.ascii_lowercase, k=4))

    # Creating new incompleteness entry
    new_entry = IncompletenessEntry(entry_id=new_entry_id, rule_code=rule_code,
                                    affected_dataclass_uri=affected_ontology_dataclass.uri,
                                    incompleteness_message=incompleteness_message)

    LOGGER.debug(f"Creating and adding new incompleteness entry: {new_entry}.")

    include_incompleteness_and_keep_updated(new_entry, incompleteness_stack)


def print_all_incompleteness(incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Print all incompleteness at the end of the execution when authorized by the user using the arguments. """

    if arguments["is_verbose"]:
        print(f"\nINCOMPLETENESS CASES IDENTIFIED: {len(incompleteness_stack)}")
        for current, incompleteness_entry in enumerate(incompleteness_stack):
            num = current + 1
            # Log incompleteness case to user if enabled by argument
            print(f"\tI{num}: rule {incompleteness_entry.rule_code}. "
                  f"Related class: {incompleteness_entry.affected_dataclass_uri}. "
                  f"{incompleteness_entry.incompleteness_message}")
