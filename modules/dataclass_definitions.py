"""Definition of dataclasses used in OntCatOWL"""
from modules.dataclass_verifications import check_duplicated_same_list_ontology, correct_number_of_elements_ontology, \
    duplicated_other_list_ontology, check_duplicated_same_list_gufo, correct_number_of_elements_gufo, \
    duplicated_other_list_gufo

if __name__ != "__main__":
    import logging
    from dataclasses import dataclass, field

    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

    # TODO (@pedropaulofb): Create expected size for each list and for the sum of each list

    @dataclass
    class OntologyClass:
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

        # TODO (@pedropaulofb): Duplicate the consistency checkings for the GUFOClass

        def is_consistent(self):
            check_duplicated_same_list_ontology(self)
            correct_number_of_elements_ontology(self)
            duplicated_other_list_ontology(self)


    @dataclass
    class GUFOClass:
        name: str = field(default_factory=str)
        is_list: list[str] = field(default_factory=list[str])
        can_list: list[str] = field(default_factory=list[str])
        not_list: list[str] = field(default_factory=list[str])

        def is_consistent(self):
            check_duplicated_same_list_gufo(self)
            correct_number_of_elements_gufo(self)
            duplicated_other_list_gufo(self)
