# Scior: Theoretical Rules

Scior has as its theoretical base a set of inference rules derived from (g)UFO's axiomatization that, given an initial classification of the classes in an OWL ontology, can support the inference of the classification for the remaining classes in the ontology. The rules are based on UFO's and gUFO's axiomatizations for endurant types, since the complete [axiomatization of UFO](https://www.sciencedirect.com/science/article/pii/S0169023X21000185?casa_token=ngGKdKhLemsAAAAA:h2AR3z30duFeLCDshD9oHuD023snHj-9ziH8jYVpb86DhjPelGS6xWLVd3FlxNZx58QfaEip6Q) was not implemented in [gUFO](https://nemo-ufes.github.io/gufo/).

While the rules are complete formalized and described in [SCIOR'S PUBLICATION](https://www.researchgate.net/publication/370527243_Inferring_Ontological_Categories_of_OWL_Classes_Using_Foundational_Rules), this document just briefly presents them in First Order Logic (FOL). Consider that all free variables are universally quantified, having all their occurring formulas as their scope. We assume that our domain of quantification only includes types.

## List of Rules

The complete list of theoretical rules is also available in `.tsv` (tab-separated) format and can be [ACCESSED HERE](https://github.com/unibz-core/Scior/blob/main/documentation/resources/rules_theoretical.tsv). The rules are:

- **R01 :**&ensp; $subClassOf(x,x)$
- **R02 :**&ensp; $subClassOf(x,y) \land subClassOf(y,z) \rightarrow subClassOf(x,z)$
- **R03 :**&ensp; $EndurantType(x) \leftrightarrow RigidType(x) \oplus NonRigidType(x)$
- **R04 :**&ensp; $NonRigidType(x) \leftrightarrow AntiRigidType(x) \oplus SemiRigidType(x)$
- **R05 :**&ensp; $EndurantType(x) \leftrightarrow Sortal(x) \oplus NonSortal(x)$
- **R06 :**&ensp; $Kind(x) \rightarrow RigidType(x) \land Sortal(x)$
- **R07 :**&ensp; $SubKind(x) \rightarrow RigidType(x) \land Sortal(x)$
- **R08 :**&ensp; $\nexists x (Kind(x) \land SubKind(x))$
- **R09 :**&ensp; $Role(x) \rightarrow AntiRigidType(x) \land Sortal(x)$
- **R10 :**&ensp; $Phase(x) \rightarrow AntiRigidType(x) \land Sortal(x)$
- **R11 :**&ensp; $\nexists x (Phase(x) \land Role(x))$
- **R12 :**&ensp; $Category(x) \rightarrow NonSortal(x) \land RigidType(x)$
- **R13 :**&ensp; $RoleMixin(x) \rightarrow NonSortal(x) \land AntiRigidType(x)$
- **R14 :**&ensp; $PhaseMixin(x) \rightarrow NonSortal(x) \land AntiRigidType(x)$
- **R15 :**&ensp; $\nexists x (PhaseMixin(x) \land RoleMixin(x))$
- **R16 :**&ensp; $Mixin(x) \rightarrow NonSortal(x) \land SemiRigidType(x)$
- **R17 :**&ensp; $RigidType(x) \rightarrow Category(x) \lor Kind(x) \lor SubKind(x)$
- **R18 :**&ensp; $AntiRigidType(x) \rightarrow Role(x) \lor Phase(x) \lor RoleMixin(x) \lor PhaseMixin(x)$
- **R19 :**&ensp; $SemiRigidType(x) \rightarrow Mixin(x)$
- **R20 :**&ensp; $Sortal(x) \rightarrow Kind(x) \lor Phase(x) \lor Role(x) \lor SubKind(x)$
- **R21 :**&ensp; $NonSortal(x) \rightarrow Category(x) \lor PhaseMixin(x) \lor RoleMixin(x) \lor Mixin(x)$
- **R22 :**&ensp; $RigidType(x) \land subClassOf(x,y) \rightarrow \neg AntiRigidType(y)$
- **R23 :**&ensp; $SemiRigidType(x) \land subClassOf(x,y) \rightarrow \neg AntiRigidType(y)$
- **R24 :**&ensp; $AntiRigidType(x) \land Sortal(x) \land Category(y) \land subClassOf(x,y) \rightarrow \exists z (RigidType(z) \land Sortal(z) \land subClassOf(x,z) \land subClassOf(z,y))$
- **R25 :**&ensp; $Mixin(x) \rightarrow \exists y,z (subClassOf(y,x) \land RigidType(y) \land subClassOf(z,x) \land AntiRigidType(z))$
- **R26 :**&ensp; $x \neq y \land Kind(x) \land subClassOf(x,y) \rightarrow NonSortal(y)$
- **R27 :**&ensp; $NonSortal(x) \land subClassOf(x,y) \rightarrow NonSortal(y)$
- **R28 :**&ensp; $Sortal(x) \rightarrow \exists! y (subClassOf (x,y) \land Kind(y))$
- **R29 :**&ensp; $shareKind(x,y) \leftrightarrow \exists! z (Kind(z) \land subClassOf(x,z) \land subClassOf(y,z))$
- **R30 :**&ensp; $shareSuperClass(x,y) \leftrightarrow \exists z (subClassOf(x,z) \land subClassOf(y,z))$
- **R31 :**&ensp; $NonSortal(x) \rightarrow \exists y, z ( y \neq z \land Sortal(y) \land Sortal(z) \land \neg shareKind(y,z) \land (subClassOf(y,x) \lor shareSuperClass(x,y)) \land (subClassOf(z,x) \lor shareSuperClass(x,z)) )$
- **R32 :**&ensp; $Phase(x) \land subClassOf(x,y) \rightarrow \neg Role(y) \land \neg RoleMixin(y)$
- **R33 :**&ensp; $PhaseMixin(x) \land subClassOf(x,y) \rightarrow \neg RoleMixin(y)$
- **R34 :**&ensp; $Role(x) \land PhaseMixin(y) \land subClassOf(x,y) \rightarrow \exists z (Phase(z) \land subClassOf(x,z) \land subClassOf(z,y))$
- **R35 :**&ensp; $Phase(x) \rightarrow \exists y (Phase (y) \land shareKind(x,y) \land \neg isSubClassOf(x,y) \land \neg isSubClassOf(y,x))$
- **R36 :**&ensp; $PhaseMixin(x) \rightarrow \exists y (Category (y) \land isSubClassOf(x,y))$
- **R37 :**&ensp; $PhaseMixin(x) \land Category(y) \land subClassOf(x,y) \rightarrow \exists z (PhaseMixin(z) \land \neg isSubClassOf(x,z) \land \neg isSubClassOf(z,x) \land isSubClassOf(z,y))$

