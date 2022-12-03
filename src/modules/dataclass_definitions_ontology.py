""" Definition of dataclass as the data structure used for loading the ontologies ontology in OntCatOWL.
    This module contains the data structure fields, initial value assignments and methods.
"""
import hashlib
from dataclasses import dataclass, field

from src.modules.dataclass_verifications import verify_duplicates_in_lists_ontology, \
    verify_single_abstract_element_available_for_types, verify_multiple_final_classifications_for_types
from src.modules.logger_config import initialize_logger
from src.modules.utils_general import lists_intersection


@dataclass
class OntologyDataClass(object):
    """ Each loaded ontology dataclass has a URI (identifier) and six lists of GUFO elements.
    The lists indicate which gufo elem. the dataclass is, can, or cannot be, for the types and individuals hierarchies.

    gufo_dictionary brings information for faster classification manipulation.

    incompleteness_info is a dictionary with the following filds:
        - is_incomplete: True or False
        - detected_in: list of rule codes where the incompleteness was detected (no repetitions are allowed).

    """

    uri: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type: list[str] = field(default_factory=list[str])
    can_individual: list[str] = field(default_factory=list[str])
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])
    gufo_dictionary: dict = field(default_factory=dict)
    incompleteness_info: dict = field(default_factory=dict)

    def is_consistent(self):
        """ Performs a consistency check on the dataclass. For now only one verification is performed, which is
         the identification of duplicates. Other verifications can be added later if necessary. """

        verify_duplicates_in_lists_ontology(self)
        verify_multiple_final_classifications_for_types(self)
        verify_single_abstract_element_available_for_types(self)

    def clear_incompleteness(self):
        "When a user define the type of the dataclass, its incompleteness status must be set to its initial state."

        self.incompleteness_info["is_incomplete"] = False
        self.incompleteness_info["detected_in"] = []

    def move_element_between_lists(self, element, source_list, target_list):
        """ Move an element between two lists in the same OntologyClass
            Elements can only be moved from CAN lists to IS or NOT lists
        """
        logger = initialize_logger()
        logger.debug(
            f"Starting to move element {element} from {source_list} list to {target_list} list in {self.uri}...")

        source = []
        target = []

        # VERIFICATION 1: Source and target lists must be different
        if source_list == target_list:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Source equals target list. Program aborted.")
            exit(1)

        # VERIFICATION 2: Only CAN lists are allowed as source list
        if source_list == "can_type":
            source = self.can_type
        elif source_list == "can_individual":
            source = self.can_individual
        else:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Source list {source_list} is unknown. Program aborted.")
            exit(1)

        # VERIFICATION 3: Only IS or NOT lists are allowed as target list
        if target_list == "is_type":
            target = self.is_type
        elif target_list == "is_individual":
            target = self.is_individual
        elif target_list == "not_type":
            target = self.not_type
        elif target_list == "not_individual":
            target = self.not_individual
        else:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Target list {target_list} is unknown. Program aborted.")
            exit(1)

        # VERIFICATION 4: Element must be in source list
        if element not in source:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. The element {element} to be moved was not found "
                         f"in {source_list}. Program aborted.")
            exit(1)

        # Move element
        source.remove(element)
        target.append(element)

        # Performs consistency check
        self.is_consistent()

        # # Updates the class after any moving, so the class can always be in an updated state
        self.update_all_internal_lists_from_gufo()

        logger.debug(f"Element {element} moved successfully from list {source_list} "
                     f"to list {target_list} in {self.uri}.")

    def move_element_to_is_list(self, element):
        """ Check if the element to be moved is a type or instance
                and move it from the corresponding CAN to the corresponding IS list.

            The element is only moved if it still not in the IS list.
            E.g. 1) if the element is in the can_type list, it is going to be moved to the is_type list.
            E.g. 2) if the element is in the is_type list, it is not going to be moved.

            This is a specific case of the move_element_between_lists method and
            is analogous to the move_element_to_not_list method.
        """

        logger = initialize_logger()

        source_list = self.return_containing_list_name(element)

        if source_list == "is_type" or source_list == "is_individual":
            logger.debug(f"Element {element} already in {source_list} for {self.uri}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "is_type"
            elif source_list == "can_individual":
                target_list = "is_individual"
            else:
                logger.error(f"Inconsistency found. Error when trying to move the element {element} to the IS LIST "
                             f"in {self.uri}. The element was not found in the CAN list. Program aborted.")
                raise Exception("INCONSISTENCY FOUND!")

            # Consistency checking is already performed inside the move_between_ontology_lists function.
            self.move_element_between_lists(element, source_list, target_list)
            self.clear_incompleteness()
            self.verify_final_type_classification()

    def move_element_to_not_list(self, element):
        """ Check if the element to be moved is a type or instance
                and move it from the corresponding CAN to the corresponding NOT list.

            The element is only moved if it still not in the NOT list.
            E.g. 1) if the element is in the can_type list, it is going to be moved to the not_type list.
            E.g. 2) if the element is in the not_type list, it is not going to be moved.

            This is a specific case of the move_element_between_lists method and
            is analogous to the move_element_to_is_list method.
        """

        logger = initialize_logger()

        source_list = self.return_containing_list_name(element)

        if source_list == "not_type" or source_list == "not_individual":
            logger.debug(f"Element {element} already in {source_list} for {self.uri}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "not_type"
            elif source_list == "can_individual":
                target_list = "not_individual"
            else:
                logger.error(f"When trying to move the element {element} to the NOT LIST in {self.uri}. "
                             f"The element was not found in the CAN list. Program aborted.")
                raise Exception("INCONSISTENCY FOUND!")

            # Consistency checking is already performed inside the move_between_ontology_lists function.
            self.move_element_between_lists(element, source_list, target_list)

    def move_list_of_elements_to_is_list(self, elem_list):
        """ Moves a list of elements to the IS list. Analogous to move_list_of_elements_to_not_list function.
        This is a specific case of the move_element_to_is_list function. """

        for elem in elem_list:
            self.move_element_to_is_list(elem)

    def move_list_of_elements_to_not_list(self, elem_list):
        """ Moves a list of elements to the NOT list. Analogous to move_list_of_elements_to_is_list function.
        This is a specific case of the move_element_to_not_list function. """

        for elem in elem_list:
            self.move_element_to_not_list(elem)

    def return_containing_list_name(self, element):
        """ Verify to which of the dataclass lists the element belongs and returns the list name. """

        logger = initialize_logger()
        containing_list_name = "not set"

        if element in self.is_type:
            containing_list_name = "is_type"
        elif element in self.is_individual:
            containing_list_name = "is_individual"
        elif element in self.can_type:
            containing_list_name = "can_type"
        elif element in self.can_individual:
            containing_list_name = "can_individual"
        elif element in self.not_type:
            containing_list_name = "not_type"
        elif element in self.not_individual:
            containing_list_name = "not_individual"
        else:
            logger.error(f"Element {element} does not belong to any list for {self.uri}. Program aborted.")
            exit(1)

        return containing_list_name

    def sort_all_internal_lists(self):
        """ Sorts all internal lists. """
        self.is_type.sort()
        self.is_individual.sort()
        self.can_type.sort()
        self.can_individual.sort()
        self.not_type.sort()
        self.not_individual.sort()

    def create_partial_hash(self, input_list):
        """ Creates a hash for a single list inside an Ontology DataClass.
            Hashes are the concatenation of all the names of all elements inside a list.
        """

        partial_hash = input_list
        list_hash = "not set"

        if input_list == "is_type":
            list_hash = self.is_type
        elif input_list == "is_individual":
            list_hash = self.is_individual
        elif input_list == "can_type":
            list_hash = self.can_type
        elif input_list == "can_individual":
            list_hash = self.can_individual
        elif input_list == "not_type":
            list_hash = self.not_type
        elif input_list == "not_individual":
            list_hash = self.not_individual
        else:
            logger = initialize_logger()
            logger.error(f"Unknown list type {input_list}. Unable to create hash. Program aborted.")
            exit(1)

        for hash_part in list_hash:
            partial_hash += hash_part

        return partial_hash

    def create_hash(self, hash_type="TOTAL"):
        """ Creates a hash of the Ontology DataClass using all its lists.
            The python builtin function hash is applied to the concatenation
                of the dataclass uri with all partial hashes of all the dataclass lists.
            The hash function can be used for verifying if the state of the class was modified after an operation.

            hash_type allowed values are:
                - TOTAL: creates a hash with all six lists of a dataclass
                - TYPES_ONLY: creates a hash with only the three types' lists of a dataclass
                - INDIVIDUALS_ONLY: creates a hash with only the three individuals' lists of a dataclass
        """

        # self.sort_all_internal_lists()

        hash_is_type = ""
        hash_is_individual = ""
        hash_can_type = ""
        hash_can_individual = ""
        hash_not_type = ""
        hash_not_individual = ""

        if (hash_type == "TOTAL") or (hash_type == "TYPES_ONLY"):
            hash_is_type = self.create_partial_hash("is_type")
            hash_can_type = self.create_partial_hash("can_type")
            hash_not_type = self.create_partial_hash("not_type")

        if (hash_type == "TOTAL") or (hash_type == "INDIVIDUALS_ONLY"):
            hash_is_individual = self.create_partial_hash("is_individual")
            hash_can_individual = self.create_partial_hash("can_individual")
            hash_not_individual = self.create_partial_hash("not_individual")

        class_hash = self.uri + hash_is_type + hash_is_individual + hash_can_type + \
                     hash_can_individual + hash_not_type + hash_not_individual

        # Used for generating fix hashes
        enc_hash = class_hash.encode('utf-8')
        final_hash = int(hashlib.sha256(enc_hash).hexdigest(), 16)

        return final_hash

    def update_all_internal_lists_from_gufo(self):
        """ Update all lists inside the Ontology DataClass using the GUFO Dictionary.
            Perform updates for is lists (type and individual) and for not lists (type and individual using complement)
        """

        logger = initialize_logger()
        logger.debug(f"Updating lists for {self.uri} using GUFO.")

        # Run only if there is any possibility for types or individuals (i.e., can list > 0).
        if len(self.can_type) > 0 or len(self.can_individual) > 0:

            hash_before = 0
            hash_after = 1

            while hash_before != hash_after:
                hash_before = self.create_hash()

                # If no element in can_type list, the solution for type was already found.
                # Update FROM TYPE (IS) LIST
                if len(self.can_type) > 0:
                    self.update_type_list_from_gufo()
                # Update FROM COMPLEMENT LIST
                if len(self.can_type) > 0:
                    self.update_complement_type()
                # Update FROM SUBTYPE LIST
                if len(self.can_type) > 0:
                    self.update_type_subtypes_negation()

                # If no element in can_individual list, the solution for individual was already found.
                # Update FROM INDIVIDUAL (IS) LIST
                if len(self.can_individual) > 0:
                    self.update_individual_list_from_gufo()
                # Update FROM COMPLEMENT LIST
                if len(self.can_individual) > 0:
                    self.update_complement_individual()
                # Update FROM SUBTYPE LIST
                if len(self.can_individual) > 0:
                    self.update_individual_subtypes_negation()

                hash_after = self.create_hash()

                if hash_before == hash_after:
                    logger.debug(f"Hash before equals hash after. Update completed for {self.uri}.")
                else:
                    logger.debug(f"Hash before NOT equals hash after. Continuing update for {self.uri}.")

    def update_type_list_from_gufo(self):
        """ Update the type list of an Ontology DataClass using the GUFO dictionary.
            This method is analogous to the update_individual_list_from_gufo method.
        """

        for is_type in self.is_type:
            new_is = self.gufo_dictionary["types"][is_type]["is_list"]
            new_not = self.gufo_dictionary["types"][is_type]["not_list"]
            self.move_list_of_elements_to_is_list(new_is)
            self.move_list_of_elements_to_not_list(new_not)

    def update_individual_list_from_gufo(self):
        """ Update the individual list of an Ontology DataClass using the GUFO dictionary.
            This method is analogous to the update_type_list_from_gufo method.
        """
        for is_individual in self.is_individual:
            new_is = self.gufo_dictionary["individuals"][is_individual]["is_list"]
            new_not = self.gufo_dictionary["individuals"][is_individual]["not_list"]
            self.move_list_of_elements_to_is_list(new_is)
            self.move_list_of_elements_to_not_list(new_not)

    def update_complement_type(self):
        """ for all elements in ontology not_list:
                the ontology dataclass element must be at list of dict keys AND
                list require_is must be subset of list is_type AND
                list require_not must be subset of list not_type, THEN
                    if all conditions are met, move the results to is_type
            Analogous to method update_complement_individual.
        """

        list_complement_keys = list(self.gufo_dictionary["complements"].keys())

        for not_type in self.not_type:
            # Condition 1: the ontology dataclass element must be at list of dict keys
            if not_type not in list_complement_keys:
                continue
            # Condition 2: list require_is must be subset of list is_type
            if not set(self.gufo_dictionary["complements"][not_type]["require_is"]).issubset(set(self.is_type)):
                continue
            # Condition 3: list require_not must be subset of list not_type
            if not set(self.gufo_dictionary["complements"][not_type]["require_not"]).issubset(set(self.not_type)):
                continue

            self.move_list_of_elements_to_is_list(self.gufo_dictionary["complements"][not_type]["result"])

    def update_complement_individual(self):
        """ for all elements in ontology not_list:
                the ontology dataclass element must be at list of dict keys AND
                list require_is must be subset of list is_individual AND
                list require_not must be subset of list not_individual, THEN
                    if all conditions are met, move the results to is_type
            Analogous to method update_complement_individual.
        """

        list_complement_keys = list(self.gufo_dictionary["complements"].keys())

        for not_individual in self.not_individual:
            # Condition 1: the ontology dataclass element must be at list of dict keys
            if not_individual not in list_complement_keys:
                continue
            # Condition 2: list require_is must be subset of list is_individual
            if not set(self.gufo_dictionary["complements"][not_individual]["require_is"]).issubset(
                    set(self.is_individual)):
                continue
            # Condition 3: list require_not must be subset of list not_individual
            if not set(self.gufo_dictionary["complements"][not_individual]["require_not"]) \
                    .issubset(set(self.not_individual)):
                continue

            self.move_list_of_elements_to_is_list(self.gufo_dictionary["complements"][not_individual]["result"])

    def update_type_subtypes_negation(self):
        """ Update the "is list" of an Ontology DataClass using the GUFO dictionary.

            General description (for types and individuals - however this method applies only to types):
            If the dataclass has in its "not lists" one of the types of the dict keys,
            then the dataclass is also not o the types of the keys' lists. E.g., if a dataclass
            is not a gufo:IntrinsicAspect, then it is also not a gufo:IntrinsicMode or a gufo:Quality.

            Subtypes assertions are already performed on methods update_(type|individual)_list_from_gufo
            Analogous to method update_individual_subtypes_negation.

        """

        list_subtypes_keys = list(self.gufo_dictionary["subtypes"].keys())

        for not_type in self.not_type:

            # Condition: the ontology dataclass element must be at list of dict keys
            if not_type in list_subtypes_keys:
                # Move all the key's list elements to the dataclass not list
                self.move_list_of_elements_to_not_list(self.gufo_dictionary["subtypes"][not_type])

    def update_individual_subtypes_negation(self):
        """ Update the "is list" of an Ontology DataClass using the GUFO dictionary.

            General description (for types and individuals - however this method applies only to individuals):
            If the dataclass has in its "not lists" one of the types of the dict keys,
            then the dataclass is also not o the types of the keys' lists. E.g., if a dataclass
            is not a gufo:IntrinsicAspect, then it is also not a gufo:IntrinsicMode or a gufo:Quality.

            Subtypes assertions are already performed on methods update_(type|individual)_list_from_gufo
            Analogous to method update_type_subtypes_negation.

        """

        list_subtypes_keys = list(self.gufo_dictionary["subtypes"].keys())

        for not_individual in self.not_individual:

            # Condition: the ontology dataclass element must be at list of dict keys
            if not_individual in list_subtypes_keys:
                # Move all the key's list elements to the dataclass not list
                self.move_list_of_elements_to_not_list(self.gufo_dictionary["subtypes"][not_individual])

    def verify_final_type_classification(self):
        """ Verifies if only a single leaf classification is present in the can_list. If this is true,
        move this leaf classification to the is list. This function applies only to the types' hierarchy.
        Justification can be found here: https://github.com/nemo-ufes/gufo/issues/7
        """

        if len(self.can_type) > 0:

            type_leaf_classifications = ["gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:Phase", "gufo:PhaseMixin",
                                         "gufo:Role", "gufo:RoleMixin", "gufo:SubKind"]

            result_list = lists_intersection(type_leaf_classifications, self.can_type)

            if len(result_list) == 1:
                self.move_element_to_is_list(result_list[0])
