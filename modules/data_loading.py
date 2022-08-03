"""Loads GUFO data used for the evaluations. In the future this module should be substituted for another data loading option, like reading a CSV, JSON, or YAML file."""

# TODO (@pedropaulofb): The data should be loaded from a structured input file, like a csv, JSON, or YAML file.

# TODO (@pedropaulofb): Create expected size for each list and for the sum of each list

if __name__ != "__main__":
    from modules.dataclass_definitions import GUFOClass


    def get_list_of_types():
        """Returns a list of dataclass GUFOClass with all GUFO types and its corresponding internal list elements"""

        gufo_types = []
        gufo_types.append(GUFOClass(name="gufo:AntiRigidType", is_list=["gufo:AntiRigidType", "gufo:NonRigidType"],
                                    can_list=["gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:Role",
                                              "gufo:RoleMixin", "gufo:Sortal"],
                                    not_list=["gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:RigidType",
                                              "gufo:SemiRigidType", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:Category", is_list=["gufo:Category", "gufo:NonSortal", "gufo:RigidType"],
                                    can_list=["gufo:Kind", "gufo:SubKind"],
                                    not_list=["gufo:AntiRigidType", "gufo:Mixin", "gufo:NonRigidType", "gufo:Phase",
                                              "gufo:PhaseMixin", "gufo:Role", "gufo:RoleMixin", "gufo:SemiRigidType",
                                              "gufo:Sortal"]))
        gufo_types.append(
            GUFOClass(name="gufo:Kind", is_list=["gufo:Kind", "gufo:RigidType", "gufo:Sortal"], can_list=[],
                      not_list=["gufo:AntiRigidType", "gufo:Category", "gufo:Mixin", "gufo:NonRigidType",
                                "gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:Role", "gufo:RoleMixin",
                                "gufo:SemiRigidType", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:Mixin",
                                    is_list=["gufo:Mixin", "gufo:NonRigidType", "gufo:NonSortal", "gufo:SemiRigidType"],
                                    can_list=[],
                                    not_list=["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Phase",
                                              "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role", "gufo:RoleMixin",
                                              "gufo:Sortal", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:NonRigidType", is_list=["gufo:NonRigidType"],
                                    can_list=["gufo:AntiRigidType", "gufo:Mixin", "gufo:NonSortal", "gufo:Phase",
                                              "gufo:PhaseMixin", "gufo:Role", "gufo:RoleMixin", "gufo:SemiRigidType",
                                              "gufo:Sortal"],
                                    not_list=["gufo:Category", "gufo:Kind", "gufo:RigidType", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:NonSortal", is_list=["gufo:NonSortal"],
                                    can_list=["gufo:AntiRigidType", "gufo:Category", "gufo:Mixin", "gufo:NonRigidType",
                                              "gufo:PhaseMixin", "gufo:RigidType", "gufo:RoleMixin",
                                              "gufo:SemiRigidType"],
                                    not_list=["gufo:Kind", "gufo:Phase", "gufo:Role", "gufo:Sortal", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:Phase",
                                    is_list=["gufo:AntiRigidType", "gufo:NonRigidType", "gufo:Phase", "gufo:Sortal"],
                                    can_list=[], not_list=["gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonSortal",
                                                           "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role",
                                                           "gufo:RoleMixin", "gufo:SemiRigidType", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:PhaseMixin",
                                    is_list=["gufo:AntiRigidType", "gufo:NonRigidType", "gufo:NonSortal",
                                             "gufo:PhaseMixin"], can_list=["gufo:Category", "gufo:RigidType"],
                                    not_list=["gufo:Kind", "gufo:Mixin", "gufo:Phase", "gufo:Role", "gufo:RoleMixin",
                                              "gufo:SemiRigidType", "gufo:Sortal", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:RigidType", is_list=["gufo:RigidType"],
                                    can_list=["gufo:Category", "gufo:Kind", "gufo:NonSortal", "gufo:Sortal",
                                              "gufo:SubKind"],
                                    not_list=["gufo:AntiRigidType", "gufo:Mixin", "gufo:NonRigidType", "gufo:Phase",
                                              "gufo:PhaseMixin", "gufo:Role", "gufo:RoleMixin", "gufo:SemiRigidType"]))
        gufo_types.append(
            GUFOClass(name="gufo:Role", is_list=["gufo:AntiRigidType", "gufo:NonRigidType", "gufo:Role", "gufo:Sortal"],
                      can_list=[], not_list=["gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonSortal", "gufo:Phase",
                                             "gufo:PhaseMixin", "gufo:RigidType", "gufo:RoleMixin",
                                             "gufo:SemiRigidType", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:RoleMixin",
                                    is_list=["gufo:AntiRigidType", "gufo:NonRigidType", "gufo:NonSortal",
                                             "gufo:RoleMixin"], can_list=["gufo:Category", "gufo:RigidType"],
                                    not_list=["gufo:Kind", "gufo:Mixin", "gufo:Phase", "gufo:PhaseMixin", "gufo:Role",
                                              "gufo:SemiRigidType", "gufo:Sortal", "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:SemiRigidType", is_list=["gufo:NonRigidType", "gufo:SemiRigidType"],
                                    can_list=["gufo:Mixin", "gufo:NonSortal", "gufo:Sortal"],
                                    not_list=["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Phase",
                                              "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role", "gufo:RoleMixin",
                                              "gufo:SubKind"]))
        gufo_types.append(GUFOClass(name="gufo:Sortal", is_list=["gufo:Sortal"],
                                    can_list=["gufo:AntiRigidType", "gufo:Kind", "gufo:NonRigidType", "gufo:Phase",
                                              "gufo:RigidType", "gufo:Role", "gufo:SemiRigidType", "gufo:SubKind"],
                                    not_list=["gufo:Category", "gufo:Mixin", "gufo:NonSortal", "gufo:PhaseMixin",
                                              "gufo:RoleMixin"]))
        gufo_types.append(
            GUFOClass(name="gufo:SubKind", is_list=["gufo:RigidType", "gufo:Sortal", "gufo:SubKind"], can_list=[],
                      not_list=["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonRigidType",
                                "gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:Role", "gufo:RoleMixin",
                                "gufo:SemiRigidType"]))
        return gufo_types


    def get_list_of_individuals():
        """Returns a list of dataclass GUFOClass with all GUFO invididuals and its corresponding internal list elements"""

        gufo_individuals = []
        gufo_individuals.append(GUFOClass(name="gufo:Aspect", is_list=["gufo:Aspect"],
                                          can_list=["gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                                                    "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Quality",
                                                    "gufo:Relator"],
                                          not_list=["gufo:Collection", "gufo:FixedCollection", "gufo:FunctionalComplex",
                                                    "gufo:Object", "gufo:Quantity", "gufo:VariableCollection"]))
        gufo_individuals.append(GUFOClass(name="gufo:Collection", is_list=["gufo:Collection", "gufo:Object"],
                                          can_list=["gufo:FixedCollection", "gufo:VariableCollection"],
                                          not_list=["gufo:Aspect", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                                                    "gufo:FunctionalComplex", "gufo:IntrinsicAspect",
                                                    "gufo:IntrinsicMode", "gufo:Quality", "gufo:Quantity",
                                                    "gufo:Relator"]))
        gufo_individuals.append(GUFOClass(name="gufo:ExtrinsicAspect", is_list=["gufo:Aspect", "gufo:ExtrinsicAspect"],
                                          can_list=["gufo:ExtrinsicMode", "gufo:Relator"],
                                          not_list=["gufo:Collection", "gufo:FixedCollection", "gufo:FunctionalComplex",
                                                    "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Object",
                                                    "gufo:Quality", "gufo:Quantity", "gufo:VariableCollection"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:ExtrinsicMode", is_list=["gufo:Aspect", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode"],
                      can_list=["gufo:IntrinsicMode", "gufo:Quality"],
                      not_list=["gufo:Collection", "gufo:FixedCollection", "gufo:FunctionalComplex",
                                "gufo:IntrinsicAspect", "gufo:Object", "gufo:Quantity", "gufo:Relator",
                                "gufo:VariableCollection"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:FixedCollection", is_list=["gufo:Collection", "gufo:FixedCollection", "gufo:Object"],
                      can_list=["gufo:ExtrinsicAspect", "gufo:ExtrinsicMode", "gufo:IntrinsicAspect",
                                "gufo:IntrinsicMode", "gufo:Quality", "gufo:Relator"],
                      not_list=["gufo:Aspect", "gufo:FunctionalComplex", "gufo:Quantity", "gufo:VariableCollection"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:FunctionalComplex", is_list=["gufo:FunctionalComplex", "gufo:Object"],
                      can_list=["gufo:FixedCollection", "gufo:VariableCollection"],
                      not_list=["gufo:Aspect", "gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                                "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Quality", "gufo:Quantity",
                                "gufo:Relator"]))
        gufo_individuals.append(GUFOClass(name="gufo:IntrinsicAspect", is_list=["gufo:Aspect", "gufo:IntrinsicAspect"],
                                          can_list=["gufo:ExtrinsicMode", "gufo:IntrinsicMode", "gufo:Quality",
                                                    "gufo:Relator"],
                                          not_list=["gufo:Collection", "gufo:ExtrinsicAspect", "gufo:FixedCollection",
                                                    "gufo:FunctionalComplex", "gufo:Object", "gufo:Quantity",
                                                    "gufo:VariableCollection"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:IntrinsicMode", is_list=["gufo:Aspect", "gufo:IntrinsicAspect", "gufo:IntrinsicMode"],
                      can_list=[],
                      not_list=["gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode", "gufo:FixedCollection",
                                "gufo:FunctionalComplex", "gufo:Object", "gufo:Quality", "gufo:Quantity",
                                "gufo:Relator", "gufo:VariableCollection"]))
        gufo_individuals.append(GUFOClass(name="gufo:Object", is_list=["gufo:Object"],
                                          can_list=["gufo:Collection", "gufo:FixedCollection", "gufo:FunctionalComplex",
                                                    "gufo:Quantity", "gufo:VariableCollection"],
                                          not_list=["gufo:Aspect", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                                                    "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Quality",
                                                    "gufo:Relator"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:Quality", is_list=["gufo:Aspect", "gufo:IntrinsicAspect", "gufo:Quality"], can_list=[],
                      not_list=["gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode", "gufo:FixedCollection",
                                "gufo:FunctionalComplex", "gufo:IntrinsicMode", "gufo:Object", "gufo:Quantity",
                                "gufo:Relator", "gufo:VariableCollection"]))
        gufo_individuals.append(GUFOClass(name="gufo:Quantity", is_list=["gufo:Object", "gufo:Quantity"],
                                          can_list=["gufo:FixedCollection", "gufo:VariableCollection"],
                                          not_list=["gufo:Aspect", "gufo:Collection", "gufo:ExtrinsicAspect",
                                                    "gufo:ExtrinsicMode", "gufo:FunctionalComplex",
                                                    "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Quality",
                                                    "gufo:Relator"]))
        gufo_individuals.append(
            GUFOClass(name="gufo:Relator", is_list=["gufo:Aspect", "gufo:ExtrinsicAspect", "gufo:Relator"],
                      can_list=["gufo:IntrinsicMode", "gufo:Quality"],
                      not_list=["gufo:Collection", "gufo:ExtrinsicMode", "gufo:FixedCollection",
                                "gufo:FunctionalComplex", "gufo:IntrinsicAspect", "gufo:Object", "gufo:Quantity",
                                "gufo:VariableCollection"]))
        gufo_individuals.append(GUFOClass(name="gufo:VariableCollection",
                                          is_list=["gufo:Collection", "gufo:Object", "gufo:VariableCollection"],
                                          can_list=[],
                                          not_list=["gufo:Aspect", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode",
                                                    "gufo:FixedCollection", "gufo:FunctionalComplex",
                                                    "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Quality",
                                                    "gufo:Quantity", "gufo:Relator"]))
        return gufo_individuals
