"""Definition of dataclasses used in OntCatOWL"""
import logging
from dataclasses import dataclass, field

from modules.dataclass_verifications import check_duplicated_same_list_ontology, correct_number_of_elements_ontology, \
    duplicated_other_list_ontology
from modules.utils_gufo import get_from_gufo_lists

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


@dataclass
class OntologyClass(object):
    """ Each loaded ontology elem. has lists of GUFO elem. (types/indivuduals) that they are, can or cannot be. """
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

        # Only a basic test were for this method
        check_duplicated_same_list_ontology(self)
        correct_number_of_elements_ontology(self)
        duplicated_other_list_ontology(self)

    def move_between_ontology_lists(self, element, source_list, target_list):
        """ Move an element between two lists in the same OntologyClass
            Elements can only be moved from CAN lists to IS or NOT lists
        """
        # TODO (@pedropaulofb): This method probably can be better implemented.

        # VERIFICATION 1: Source and target lists must be different
        if source_list == target_list:
            logging.error("Source equals target list. Program aborted.")
            exit(1)

        # VERIFICATION 2: Only CAN lists are allowed as source list
        if source_list == "can_type":
            source = self.can_type
        elif source_list == "can_individual":
            source = self.can_individual
        else:
            logging.error(f"Source list {source_list} is unknown. Program aborted.")
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
            logging.error(f"Target list {target_list} is unknown. Program aborted.")
            exit(1)

        # VERIFICATION 4: Element must be in source list
        if element not in source:
            logging.error(f"The element {element} to be moved was not found in {source_list}. Program aborted.")
            exit(1)

        # Move element
        logging.debug(f"Moving element {element} from {source_list} list to {target_list} list in {self.uri}.")
        source.remove(element)
        target.append(element)

        # Performs consistency check - if time-consuming, this operation can be removed
        self.is_consistent()

        logging.debug("Element moved successfully.")

    # TODO (@pedropaulofb): Not tested yet.
    def move_to_is_list(self, element):
        """ Check if the element to be moved is a type or instance and move it from the CAN to the IS list.
            This is a specific case of the move_between_ontology_lists function.
        """

        source_list = self.return_containing_list_name(element)

        if source_list == "can_type":
            target_list = "is_type"
        elif source_list == "can_instance":
            target_list = "is_instance"
        else:
            logging.error(f"When trying to move the element {element} to the IS LIST, "
                          f"it was not found in the CAN list. Program aborted.")
            exit(1)

        # Consistency checking is already performed inside the move_between_ontology_lists function.
        self.move_between_ontology_lists(element, source_list, target_list)

    # TODO (@pedropaulofb): Not tested yet.
    def move_to_not_list(self, element):
        """ Check if the element to be moved is a type or instance and move it from the CAN to the NOT list.
            This is a specific case of the move_between_ontology_lists function.
        """

        source_list = self.return_containing_list_name(element)

        if source_list == "can_type":
            target_list = "not_type"
        elif source_list == "can_instance":
            target_list = "not_instance"
        else:
            logging.error(f"When trying to move the element {element} to the NOT LIST, "
                          f"it was not found in the CAN list. Program aborted.")
            exit(1)

        # Consistency checking is already performed inside the move_between_ontology_lists function.
        self.move_between_ontology_lists(element, source_list, target_list)

    def return_containing_list_name(self, element):
        """ Verify to which of the dataclass lists the element belongs and returns the list name. """

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
            logging.error(f"Element does not belong to any list for {self.uri}. Program aborted.")
            exit(1)

        return containing_list

    def create_partial_hash(self, input_list):
        """ Creates a hash for a single list of the OntologyClass. """

        partial_hash = input_list

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
            logging.error("Unknown list type. Unable to create hash. Program aborted.")
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

        logging.debug(f"Hash successfully created for {self.uri}.")

        return class_hash

    # TODO (@pedropaulofb): Not tested yet. Test it.
    def update_lists_from_gufo(self, gufo_types, gufo_individuals):

        logging.debug(f"Updating lists for {self.uri} using GUFO.")

        hash_before = "hash BEFORE not set"
        hash_after = "hash AFTER not set"

        while hash_before != hash_after:
            hash_before = self.create_hash()
            for it in range(len(self.is_type)):
                new_is, new_not = get_from_gufo_lists(self.is_type[it], gufo_types)
                for jt in range(len(new_is)):
                    if new_is[jt] not in self.is_type:
                        self.move_to_is_list(new_is[jt])
                for kt in range(len(new_not)):
                    if new_not[kt] not in self.not_type:
                        self.move_to_not_list(new_not[kt])
            for ii in range(len(self.is_individual)):
                new_is, new_not = get_from_gufo_lists(self.is_individual[ii], gufo_individuals)
                for ji in range(len(new_is)):
                    if new_is[ji] not in self.is_individual[ii]:
                        self.move_to_is_list(new_is[ji])
                for ki in range(len(new_not)):
                    if new_not[ki] not in self.not_individual:
                        self.move_to_not_list(new_not[ki])
            hash_after = self.create_hash()
            if hash_before == hash_after:
                logging.debug(f"Hash before equals hash after. Update completed for {self.uri}.")
            else:
                logging.debug(f"Hash before NOT equals hash after. Continuing update for {self.uri}.")
                              # f"\nHASH BEFORE = {hash_before}"
                              # f"\nHASH AFTER = {hash_after}")
