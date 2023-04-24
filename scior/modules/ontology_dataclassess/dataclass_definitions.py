""" Definition of dataclass as the data structure used for loading the ontologies ontology in Scior.
    This module contains the data structure fields, initial value assignments and methods.
"""
from dataclasses import dataclass, field

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


@dataclass
class OntologyDataClass(object):
    """ Each loaded ontology dataclass has a URI (identifier) and six lists of GUFO elements.
        Lists indicate which gUFO element the dataclass is, can, or cannot be for the types and individuals hierarchies.
    """

    uri: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type: list[str] = field(default_factory=list[str])
    can_individual: list[str] = field(default_factory=list[str])
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])

    def sort_all_internal_lists(self):
        """ Sorts all internal lists. """
        self.is_type.sort()
        self.is_individual.sort()
        self.can_type.sort()
        self.can_individual.sort()
        self.not_type.sort()
        self.not_individual.sort()
