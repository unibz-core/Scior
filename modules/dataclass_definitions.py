"""Definition of dataclasses used in OntCatOWL"""
from modules.dataclass_verifications import check_duplicated_same_list_ontology, correct_number_of_elements_ontology, \
    duplicated_other_list_ontology, check_duplicated_same_list_gufo, correct_number_of_elements_gufo, \
    duplicated_other_list_gufo

if __name__ != "__main__":
    import logging
    from dataclasses import dataclass, field

    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


    @dataclass
    class OntologyClass(object):
        """ Each loaded ontology elem. has lists of GUFO elem. (types/indivuduals) that they are, can or cannot be. """
        name: str = field(default_factory=str)
        is_type: list[str] = field(default_factory=list[str])
        is_individual: list[str] = field(default_factory=list[str])
        can_type = ["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonRigidType",
                    "gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role", "gufo:RoleMixin",
                    "gufo:SemiRigidType", "gufo:Sortal", "gufo:SubKind"]
        can_individual = ["gufo:Aspect", "gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                          "gufo:FixedCollection", "gufo:FunctionalComplex", "gufo:IntrinsicAspect",
                          "gufo:IntrinsicMode", "gufo:Object", "gufo:Quality", "gufo:Quantity", "gufo:Relator",
                          "gufo:VariableCollection"]
        not_type: list[str] = field(default_factory=list[str])
        not_individual: list[str] = field(default_factory=list[str])

        def is_consistent(self):
            # CAUTION: FUNCTIONS NOT TESTED YET!
            check_duplicated_same_list_ontology(self)
            correct_number_of_elements_ontology(self)
            duplicated_other_list_ontology(self)


    @dataclass
    class GUFOClass(object):
        """ Each GUFO element has a list of other GUFO elements that they are, can be or cannot be. """
        name: str = field(default_factory=str)
        is_list: list[str] = field(default_factory=list[str])
        can_list: list[str] = field(default_factory=list[str])
        not_list: list[str] = field(default_factory=list[str])

        def is_consistent(self):
            # basic test ok
            check_duplicated_same_list_gufo(self)
            # basic test ok
            correct_number_of_elements_gufo(self)
            # basic test ok
            duplicated_other_list_gufo(self)
