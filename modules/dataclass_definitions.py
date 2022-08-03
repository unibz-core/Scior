"""Definition of dataclasses used in OntCatOWL"""

if __name__ != "__main__":
    import logging
    from dataclasses import dataclass, field

    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


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

        # def is_consistent(self):
        #     duplicated_same_list(self)
        #     correct_number_of_elements(self)
        #     duplicated_other_list(self)  # There is no need to return True, because a false validation exits the execution with an error message.


    @dataclass
    class GUFOClass:
        name: str = field(default_factory=str)
        is_list: list[str] = field(default_factory=list[str])
        can_list: list[str] = field(default_factory=list[str])
        not_list: list[str] = field(default_factory=list[str])

        # TODO (@pedropaulofb): VERIFICATION - Copy code from OWLClass
