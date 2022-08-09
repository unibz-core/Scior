"""Definition of dataclasses used in OntCatOWL"""

import logging
from dataclasses import dataclass, field

from modules.dataclass_verifications import check_duplicated_same_list_gufo, correct_number_of_elements_gufo, \
    duplicated_other_list_gufo

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


@dataclass
class GUFOClass(object):
    """ Each GUFO element has a list of other GUFO elements that they are, can be or cannot be. """
    uri: str = field(default_factory=str)
    is_list: list[str] = field(default_factory=list[str])
    can_list: list[str] = field(default_factory=list[str])
    not_list: list[str] = field(default_factory=list[str])

    def is_consistent(self):
        """ Performs a consistency check on the dataclass """
        # Only a basic test were for this method
        check_duplicated_same_list_gufo(self)
        correct_number_of_elements_gufo(self)
        duplicated_other_list_gufo(self)
