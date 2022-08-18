"""Definition of dataclasses used in OntCatOWL"""
from dataclasses import dataclass, field

from modules.dataclass_verifications import check_duplicated_same_list_ontology, correct_number_of_elements_ontology, \
    duplicated_other_list_ontology
from modules.logger_config import initialize_logger
from modules.utils_gufo import get_from_gufo_lists


@dataclass
class OntologyClass(object):
    """ Each loaded ontology elem. has lists of GUFO elem. (types/individuals) that they are, can or cannot be. """
    uri: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type: list[str] = field(default_factory=list[str])
    can_individual: list[str] = field(default_factory=list[str])
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])

    def __post_init__(self):
        self.can_type = ["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonRigidType",
                         "gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role",
                         "gufo:RoleMixin", "gufo:SemiRigidType", "gufo:Sortal", "gufo:SubKind"]
        self.can_individual = ["gufo:Aspect", "gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                               "gufo:FixedCollection", "gufo:FunctionalComplex", "gufo:IntrinsicAspect",
                               "gufo:IntrinsicMode", "gufo:Object", "gufo:Quality", "gufo:Quantity", "gufo:Relator",
                               "gufo:VariableCollection"]

    def is_consistent(self):
        """ Performs a consistency check on the dataclass """

        check_duplicated_same_list_ontology(self)
        correct_number_of_elements_ontology(self)
        duplicated_other_list_ontology(self)

    def move_element_between_lists(self, element, source_list, target_list):
        """ Move an element between two lists in the same OntologyClass
            Elements can only be moved from CAN lists to IS or NOT lists
        """

        logger = initialize_logger()
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
        if element not in source_list:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. The element {element} to be moved was not found "
                         f"in {source_list}. Program aborted.")
            exit(1)

        # Move element
        logger.debug(f"Moving element {element} from {source_list} list to {target_list} list in {self.uri}.")
        source.remove(element)
        target.append(element)

        # Performs consistency check - if time-consuming, this operation can be removed
        self.is_consistent()

        logger.debug(f"Element {element} moved successfully from list {source_list} to list {target_list}.")

    def move_element_to_is_list(self, element):
        """ Check if the element to be moved is a type or instance and move it from the CAN to the IS list.
            The element is only moved it if it still not in the IS list.
            This is a specific case of the move_element_between_lists function.
        """
        logger = initialize_logger()
        target_list = "undefined"

        source_list = self.return_containing_list_name(element)

        if source_list == "is_type" or source_list == "is_individual":
            logger.debug(f"Element {element} already in {source_list}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "is_type"
            elif source_list == "can_individual":
                target_list = "is_individual"
            else:
                logger.error(f"When trying to move the element {element} to the IS LIST, "
                             f"it was not found in the CAN list. Program aborted.")
                exit(1)

        # Consistency checking is already performed inside the move_between_ontology_lists function.
        self.move_element_between_lists(element, source_list, target_list)

    def move_element_to_not_list(self, element):
        """ Check if the element to be moved is a type or instance and move it from the CAN to the NOT list.
            The element is only moved it if it still not in the NOT list.
            This is a specific case of the move_element_between_lists function.
        """

        logger = initialize_logger()
        target_list = "undefined"

        source_list = self.return_containing_list_name(element)

        if source_list == "not_type" or source_list == "not_individual":
            logger.debug(f"Element {element} already in {source_list}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "not_type"
            elif source_list == "can_individual":
                target_list = "not_individual"
            else:
                logger.error(f"When trying to move the element {element} to the NOT LIST, "
                             f"it was not found in the CAN list. Program aborted.")
                exit(1)

        # Consistency checking is already performed inside the move_between_ontology_lists function.
        self.move_element_between_lists(element, source_list, target_list)

    def move_elem_list_to_is_list(self, elem_list):
        """ Move a list of elements to the IS list """
        for i in range(len(elem_list)):
            self.move_element_to_is_list(elem_list[i])

    def move_elem_list_to_not_list(self, elem_list):
        """ Move a list of elements to the NOT list """
        for i in range(len(elem_list)):
            self.move_element_to_not_list(elem_list[i])

    def return_containing_list_name(self, element):
        """ Verify to which of the dataclass lists the element belongs and returns the list name. """

        logger = initialize_logger()
        containing_list = "not set"

        if element in self.is_type:
            containing_list = "is_type"
        elif element in self.is_individual:
            containing_list = "is_individual"
        elif element in self.can_type:
            containing_list = "can_type"
        elif element in self.can_individual:
            containing_list = "can_individual"
        elif element in self.not_type:
            containing_list = "not_type"
        elif element in self.not_individual:
            containing_list = "not_individual"
        else:
            logger.error(f"Element {element} does not belong to any list for {self.uri}. Program aborted.")
            exit(1)

        logger.debug(f"Element {element} currently belong to list {containing_list} for {self.uri}.")

        return containing_list

    def create_partial_hash(self, input_list):
        """ Creates a hash for a single list of the OntologyClass. """

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
            logger.error("Unknown list type. Unable to create hash. Program aborted.")
            exit(1)

        for i in range(len(list_hash)):
            partial_hash += list_hash[i]

        return partial_hash

    def create_hash(self):
        """ Creates a hash of the OntologyClass using all its lists.
            The hash function can be used for verifying if the state of the class was modified after an operation.
            Hash format is the name of the lists concatenated with the name of all its internal elements.
        """

        hash_is_type = self.create_partial_hash("is_type")
        hash_is_individual = self.create_partial_hash("is_individual")
        hash_can_type = self.create_partial_hash("can_type")
        hash_can_individual = self.create_partial_hash("can_individual")
        hash_not_type = self.create_partial_hash("not_type")
        hash_not_individual = self.create_partial_hash("not_individual")

        class_hash = hash_is_type + hash_is_individual + hash_can_type + hash_can_individual + \
                     hash_not_type + hash_not_individual

        logger = initialize_logger()
        logger.debug(f"Hash successfully created for {self.uri}.")

        return class_hash

    def update_lists_from_gufo(self, gufo_types, gufo_individuals):

        logger = initialize_logger()
        logger.debug(f"Updating lists for {self.uri} using GUFO.")

        hash_before = "hash BEFORE not set"
        hash_after = "hash AFTER not set"

        while hash_before != hash_after:
            hash_before = self.create_hash()
            for it in range(len(self.is_type)):
                new_is, new_not = get_from_gufo_lists(self.is_type[it], gufo_types)
                self.move_elem_list_to_is_list(new_is)
                self.move_elem_list_to_not_list(new_not)
            for ii in range(len(self.is_individual)):
                new_is, new_not = get_from_gufo_lists(self.is_individual[ii], gufo_individuals)
                self.move_elem_list_to_is_list(new_is)
                self.move_elem_list_to_not_list(new_not)
            hash_after = self.create_hash()
            if hash_before == hash_after:
                logger.debug(f"Hash before equals hash after. Update completed for {self.uri}.")
            else:
                logger.debug(f"Hash before NOT equals hash after. Continuing update for {self.uri}.")
