"""Definition of data structures for OntCatOWL"""
from dataclasses import dataclass, field

@dataclass
class OwlClass:
    name: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type = ["gufo:AntiRigidType", "gufo:Category", "gufo:Kind", "gufo:Mixin", "gufo:NonRigidType", "gufo:NonSortal", "gufo:Phase", "gufo:PhaseMixin", "gufo:RigidType", "gufo:Role", "gufo:RoleMixin", "gufo:SemiRigidType", "gufo:Sortal", "gufo:SubKind"]
    can_individual = ["gufo:Aspect", "gufo:Collection", "gufo:ExtrinsicAspect", "gufo:ExtrinsicMode", "gufo:FixedCollection", "gufo:FunctionalComplex", "gufo:IntrinsicAspect", "gufo:IntrinsicMode", "gufo:Object", "gufo:Quality", "gufo:Quantity", "gufo:Relator", "gufo:VariableCollection"]
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])


def initialize_gufo_list(gufo_list):
    print("Initializing GUFO list.")
    return gufo_list