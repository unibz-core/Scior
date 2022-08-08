"""Definition of dataclasses used in OntCatOWL"""
from modules.dataclass_verifications import check_duplicated_same_list_ontology, correct_number_of_elements_ontology, \
    duplicated_other_list_ontology

if __name__ != "__main__":
    import logging
    from dataclasses import dataclass, field

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

        def move_between_lists(self, element, source_list, target_list):
            """ Move an element between two lists in the same OntologyClass """
            # TODO (@pedropaulofb): This method probably can be better implemented.

            # Source and target lists must be different
            if source_list == target_list:
                logging.error("Source equals target list. Program aborted.")
                exit(1)

            if source_list == "is_type":
                source = self.is_type
            elif source_list == "is_individual":
                source = self.is_individual
            elif source_list == "can_type":
                source = self.can_type
            elif source_list == "can_individual":
                source = self.can_individual
            elif source_list == "not_type":
                source = self.not_type
            elif source_list == "not_individual":
                source = self.not_individual
            else:
                logging.error("Unknown source list type. Program aborted.")
                exit(1)

            if target_list == "is_type":
                target = self.is_type
            elif target_list == "is_individual":
                target = self.is_individual
            elif target_list == "can_type":
                target = self.can_type
            elif target_list == "can_individual":
                target = self.can_individual
            elif target_list == "not_type":
                target = self.not_type
            elif target_list == "not_individual":
                target = self.not_individual
            else:
                logging.error("Unknown target list type. Program aborted.")
                exit(1)

            # Element must be in source list
            if element not in source:
                logging.error("The element to be moved was not found in source list. Program aborted.")
                exit(1)

            # Move element
            logging.debug(f"Moving element {element} from {source_list} list to {target_list} list in {self.uri}. "
                          f"Program aborted.")
            source.remove(element)
            target.append(element)

            # Performs consistency check - if time-consuming, this operation can be removed
            self.is_consistent()

            logging.debug("Element moved successfully.")

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
                logging.error(f"Element doesnt belong to any list for {self.uri}. Program aborted.")
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

            class_hash = hash_is_type + hash_is_individual + hash_can_type + hash_can_individual + hash_not_type + hash_not_individual

            logging.debug(f"Hash successfully created for {self.uri}.")

            return class_hash

        # TODO (@pedropaulofb): To be implemented.
        def update_lists_from_gufo(self):

            # access corresponding GUFO element list
            # for all NOT, move from where they are to the NOT list
            # BEFORE MOVING: check if IS = NOT, if so INCONSISTENCY
            # for all IS, move from where they are to the IS list
            # BEFORE MOVING: check if IS = NOT, if so INCONSISTENCY
            # Run on modified elements up to there is no modification (hash before and hash after)

            return self
