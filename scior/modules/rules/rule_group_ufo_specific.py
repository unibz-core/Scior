""" Implementation of rules of group UFO Specific. """

from scior.modules.logger_config import initialize_logger

logger = initialize_logger()

def execute_rules_ufo_specific(ontology_graph):
    """Executes all rules of the UFO Specific group."""
    pass

# R24Cs: \exists! z (AntiRigidType(x) \land Sortal(x) \land Category(y) \land subClassOf(x,y) \land subClassOf(x,z) \land subClassOf(z,y) \rightarrow RigidType(z) \land Sortal(z))
# R25Cs1: \exists! z (Mixin(x) \land subClassOf(y,x) \land RigidType(y) \land subClassOf(z,x) \rightarrow AntiRigidType(z))
# R25Cs2: \exists! y (Mixin(x) \land subClassOf(y,x) \land AntiRigidType(z) \land subClassOf(z,x) \rightarrow RigidType(y))
# R28Cs: \exists! y (Sortal(x) \land subClassOf (x,y) \rightarrow Kind(y))
# R29Cs: \exists! z (shareKind(x,y) \land subClassOf(x,z) \land subClassOf(y,z) \rightarrow Kind(z))
# R31Cs: \exists! y, z (y \neq z \land NonSortal(x) \land \neg shareKind(y,z) \land (subClassOf(y,x) \lor shareSuperClass(x,y)) \land (subClassOf(z,x) \lor shareSuperClass(x,z)) \rightarrow Sortal(y) \land Sortal(z))
# R34Cs: \exists! z (Role(x) \land PhaseMixin(y) \land subClassOf(x,y) \land subClassOf(x,z) \land subClassOf(z,y) \rightarrow Phase(z))
# R35Cs: \exists! y (Phase(x) \land shareKind(x,y) \land \neg isSubClassOf(x,y) \land \neg isSubClassOf(y,x) \rightarrow Phase(y))
# R36Cs: \exists! y (PhaseMixin(x) \land isSubClassOf(x,y) \rightarrow Category (y))
# R37Cs: \exists! z (PhaseMixin(x) \land Category(y) \land subClassOf(x,y) \land \neg isSubClassOf(x,z) \land \neg isSubClassOf(z,x) \land isSubClassOf(z,y) \rightarrow PhaseMixin(z))

