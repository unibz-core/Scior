# Scior: Implemented Rules

The rules implemented in Scior are outlined in this document.

## Content

- [Scior: Implemented Rules](#scior-implemented-rules)
  - [Content](#content)
  - [Definitions](#definitions)
    - [Scope](#scope)
    - [Groups of Rules](#groups-of-rules)
    - [Nomenclature for Rules](#nomenclature-for-rules)
  - [Implementation Rules](#implementation-rules)
    - [Auxiliary Rules Group](#auxiliary-rules-group)
    - [Base Rules Group](#base-rules-group)
    - [CWA Rules Group](#cwa-rules-group)
    - [gUFO Leaves Rules Group](#gufo-leaves-rules-group)
    - [gUFO Negative Rules Group](#gufo-negative-rules-group)
    - [gUFO Positive Rules Group](#gufo-positive-rules-group)
    - [UFO All Rules Group](#ufo-all-rules-group)
    - [UFO Some Rules Group](#ufo-some-rules-group)
    - [UFO Unique Rules Group](#ufo-unique-rules-group)


## Definitions

### Scope

The current version of the Scior is limited to Endurant types. I.e., there are no rules implemented for other ontological categories provided by [the Unified Foundational Ontology (UFO)](https://philpapers.org/archive/PORUUF.pdf). Even though gUFO has two taxonomies (one with classes whose instances are individuals and another with classes whose instances are types), because of this restriction, only the latter is handled by the rules here presented—more specifically, Scior uses the [Endurant types](https://nemo-ufes.github.io/gufo/#enduranttypes) part of the types hierarchy. This hierarchy addresses two ontological meta-properties of entities: [sortality](https://ontouml.readthedocs.io/en/latest/theory/identity.html) (related to the *identity principle* the entity may provide or carry) and [rigidity](https://ontouml.readthedocs.io/en/latest/theory/rigidity.html).

### Groups of Rules

| Group         | **Code** | **Definition**                                                                                |
|---------------|----------|-----------------------------------------------------------------------------------------------|
| Auxiliary     | X        | Rules to support other groups of rules and that are executed multiple times.                  |
| Base          | B        | Rules to support other groups of rules and that are executed only once.                       |
| CWA           | C        | Rules applied only when Scior is set up in CWA mode.                                          |
| gUFO Leaves   | L        | The rule's consequent part defines a class's final gUFO classification (leaf classification). |
| gUFO Negative | N        | Rules comprising negative assertions about gUFO classifications on their consequent.          |
| gUFO Positive | P        | Rules comprising positive assertions about gUFO classifications on their consequent.          |
| UFO All       | A        | Rules derived from UFO and that comprise universal quantification.                            |
| UFO Some      | S        | Rules derived from UFO and that comprise existential quantification.                          |
| UFO Unique    | U        | Rules derived from UFO and that comprise uniqueness quantification.                           |

### Nomenclature for Rules

Three agglutinated elements compose the rules' codes: *prefix*, *letter code*, and *number code*.

- Prefixes are always the capital letter R.

- The letter code is defined by the rule's group and can be observed in the presented group table.

- The number code has two digits and is serial within each group.

Example of codes are: RA01, RL10, and RU02.

## Implementation Rules

A complete list of implementation rules is available in `.tsv` (tab-separated) format here.

### Auxiliary Rules Group

- **RX01 :**&ensp; $Kind(z) \land subClassOf(x,z) \land subClassOf(y,z) \rightarrow shareKind(x,y)$
- **RX02 :**&ensp; $Kind(z) \land subClassOf(x,z) \land shareKind(x,y) \rightarrow subClassOf(y,z)$

### Base Rules Group

- **RB01 :**&ensp; $subClassOf(x,x)$
- **RB02 :**&ensp; $subClassOf(x,y) \land subClassOf(y,z) \rightarrow subClassOf(x,z)$
- **RB03 :**&ensp; $subClassOf(x,z) \land subClassOf(y,z) \rightarrow shareSuperClass(x,y)$

### CWA Rules Group

- **RC01 :**&ensp; $\neg (\exists z (RigidType(z) \land Sortal(z) \land subClassOf(x,z) \land subClassOf(z,y))) \land AntiRigidType(x) \land Sortal(x) \land subClassOf(x,y) \rightarrow \neg Category(y)$
- **RC02 :**&ensp; $\neg (\exists y, z (subClassOf(y,x) \land AntiRigidType(y) \land subClassOf(z,x) \land RigidType(z))) \rightarrow \neg Mixin(x)$
- **RC03 :**&ensp; $\neg(\exists y (x \neq y \land subClassOf(x,y)) \rightarrow Kind(x))$
- **RC04 :**&ensp; $\neg (\exists y (subClassOf (x,y) \land Kind(y))) \rightarrow \neg Sortal(x)$
- **RC05 :**&ensp; $\neg (\exists y, z ( y \neq z \land Sortal(y) \land Sortal(z) \land \neg shareKind(y,z) \land (subClassOf(y,x) v shareSuperClass(x,y))) \land (subClassOf(z,x) v shareSuperClass(x,z))) \rightarrow \neg NonSortal(x)$
- **RC06 :**&ensp; $\neg (\exists z (Phase(z) \land subClassOf(x,z) \land subClassOf(z,y))) \land Role(x) \land subClassOf(x,y) \rightarrow \neg PhaseMixin(y)$
- **RC07 :**&ensp; $\neg (\exists z (Phase(z) \land subClassOf(x,z) \land subClassOf(z,y))) \land PhaseMixin(y) \land subClassOf(x,y) \rightarrow \neg Role(x)$
- **RC08 :**&ensp; $\neg (\exists y (Phase (y) \land shareKind(x,y) \land \neg isSubClassOf(x,y) \land \neg isSubClassOf(y,x))) \rightarrow \neg Phase(x)$
- **RC09 :**&ensp; $\neg (\exists y (Category (y) \land isSubClassOf(x,y))) \rightarrow \neg PhaseMixin(x)$
- **RC10 :**&ensp; $\neg (\exists z (PhaseMixin(z) \land Category(y) \land subClassOf(x,y) \land \neg isSubClassOf(x,z) \land \neg isSubClassOf(z,x) \land isSubClassOf(z,y))) \rightarrow \neg PhaseMixin(x)$
- **RC11 :**&ensp; $\neg (\exists z (PhaseMixin(z) \land PhaseMixin(x) \land subClassOf(x,y) \land \neg isSubClassOf(x,z) \land \neg isSubClassOf(z,x) \land isSubClassOf(z,y))) \rightarrow \neg Category(y)$

### gUFO Leaves Rules Group

- **RL01 :**&ensp; $RigidType(x) \land \neg Kind(x) \land \neg SubKind(x) \rightarrow Category(x)$
- **RL02 :**&ensp; $RigidType(x) \land \neg SubKind(x) \land \neg Category(x) \rightarrow Kind(x)$
- **RL03 :**&ensp; $RigidType(x) \land \neg Kind(x) \land \neg Category(x) \rightarrow SubKind(x)$
- **RL04 :**&ensp; $AntiRigidType(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x) \rightarrow Role(x)$
- **RL05 :**&ensp; $AntiRigidType(x) \land \neg Role(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x) \rightarrow Phase(x)$
- **RL06 :**&ensp; $AntiRigidType(x) \land \neg Role(x) \land \neg Phase(x) \land \neg PhaseMixin(x) \rightarrow RoleMixin(x)$
- **RL07 :**&ensp; $AntiRigidType(x) \land \neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \rightarrow PhaseMixin(x)$
- **RL08 :**&ensp; $Sortal(x) \land \neg Phase(x) \land \neg Role(x) \land \neg SubKind(x) \rightarrow Kind(x)$
- **RL09 :**&ensp; $Sortal(x) \land \neg Kind(x) \land \neg Role(x) \land \neg SubKind(x) \rightarrow Phase(x)$
- **RL10 :**&ensp; $Sortal(x) \land \neg Kind(x) \land \neg Phase(x) \land \neg SubKind(x) \rightarrow Role(x)$
- **RL11 :**&ensp; $Sortal(x) \land \neg Kind(x) \land \neg Phase(x) \land \neg Role(x) \rightarrow SubKind(x)$
- **RL12 :**&ensp; $NonSortal(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg Mixin(x) \rightarrow Category(x)$
- **RL13 :**&ensp; $NonSortal(x) \land \neg Category(x) \land \neg RoleMixin(x) \land \neg Mixin(x) \rightarrow PhaseMixin(x)$
- **RL14 :**&ensp; $NonSortal(x) \land \neg Category(x) \land \neg PhaseMixin(x) \land \neg Mixin(x) \rightarrow RoleMixin(x)$
- **RL15 :**&ensp; $NonSortal(x) \land \neg Category(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \rightarrow Mixin(x)$

### gUFO Negative Rules Group

- **RN01 :**&ensp; $\neg NonRigidType(x) \rightarrow RigidType(x)$
- **RN02 :**&ensp; $\neg AntiRigidType(x) \land \neg SemiRigidType(x) \rightarrow RigidType(x)$
- **RN03 :**&ensp; $\neg Category(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x) \rightarrow SemiRigidType(x)$
- **RN04 :**&ensp; $\neg Category(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Mixin(x) \rightarrow AntiRigidType(x)$
- **RN05 :**&ensp; $\neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x) \land \neg Mixin(x) \rightarrow RigidType(x)$
- **RN06 :**&ensp; $\neg RigidType(x) \rightarrow NonRigidType(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Category(x)$
- **RN07 :**&ensp; $\neg Sortal(x) \rightarrow NonSortal(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Role(x) \land \neg Phase(x)$
- **RN08 :**&ensp; $\neg NonSortal(x) \rightarrow Sortal(x) \land \neg Category(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg Mixin(x)$
- **RN09 :**&ensp; $\neg Kind(x) \land \neg Phase(x) \land \neg Role(x) \land \neg SubKind(x) \rightarrow NonSortal(x)$
- **RN10 :**&ensp; $\neg Category(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg Mixin(x) \rightarrow Sortal(x)$
- **RN11 :**&ensp; $\neg AntiRigidType(x) \rightarrow \neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x)$
- **RN12 :**&ensp; $\neg Mixin(x) \rightarrow \neg SemiRigidType$

### gUFO Positive Rules Group

- **RP01 :**&ensp; $NonRigidType(x) \rightarrow \neg RigidType(x)$
- **RP02 :**&ensp; $RigidType(x) \rightarrow \neg NonRigidType(x) \land \neg AntiRigidType(x) \land \neg SemiRigidType(x) \land \neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x) \land \neg Mixin(x)$
- **RP03 :**&ensp; $AntiRigidType(x) \rightarrow NonRigidType(x) \land \neg SemiRigidType(x) \land \neg Category(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Mixin(x)$
- **RP04 :**&ensp; $SemiRigidType(x) \rightarrow Mixin(x) \land NonRigidType(x) \land \neg AntiRigidType(x) \land \neg Category(x) \land \neg Kind(x) \land \neg SubKind(x) \land \neg Role(x) \land \neg Phase(x) \land \neg RoleMixin(x) \land \neg PhaseMixin(x)$
- **RP05 :**&ensp; $NonSortal(x) \rightarrow \neg Sortal(x) \land \neg Kind(x) \land \neg Phase(x) \land \neg Role(x) \land \neg SubKind(x)$
- **RP06 :**&ensp; $Sortal(x) \rightarrow \neg NonSortal(x) \land \neg Category(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg Mixin(x)$
- **RP07 :**&ensp; $Kind(x) \rightarrow RigidType(x) \land Sortal(x) \land \neg Category(x) \land \neg Phase(x) \land \neg Role(x) \land \neg SubKind(x)$
- **RP08 :**&ensp; $SubKind(x) \rightarrow RigidType(x) \land Sortal(x) \land \neg Category(x) \land \neg Kind(x) \land \neg Phase(x) \land \neg Role(x)$
- **RP09 :**&ensp; $Role(x) \rightarrow AntiRigidType(x) \land Sortal(x) \land \neg Kind(x) \land \neg Phase(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg SubKind(x)$
- **RP10 :**&ensp; $Phase(x) \rightarrow AntiRigidType(x) \land Sortal(x) \land \neg Kind(x) \land \neg PhaseMixin(x) \land \neg Role(x) \land \neg RoleMixin(x) \land \neg SubKind(x) $
- **RP11 :**&ensp; $Category(x) \rightarrow NonSortal(x) \land RigidType(x) \land \neg Kind(x) \land \neg Mixin(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x) \land \neg SubKind(x)$
- **RP12 :**&ensp; $RoleMixin(x) \rightarrow AntiRigidType(x) \land NonSortal(x) \land \neg Category(x) \land \neg Mixin(x) \land \neg Phase(x) \land \neg PhaseMixin(x) \land \neg Role(x)$
- **RP13 :**&ensp; $PhaseMixin(x) \rightarrow AntiRigidType(x) \land NonSortal(x) \land \neg Category(x) \land \neg Mixin(x) \land \neg Phase(x) \land \neg Role(x) \land \neg RoleMixin(x)$
- **RP14 :**&ensp; $Mixin(x) \rightarrow NonSortal(x) \land SemiRigidType(x) \land \neg Category(x) \land \neg PhaseMixin(x) \land \neg RoleMixin(x)$

### UFO All Rules Group

- **RA01 :**&ensp; $Sortal(x) \land subClassOf(y,x) \rightarrow Sortal(y)$
- **RA02 :**&ensp; $RigidType(x) \land subClassOf(x,y) \rightarrow \neg AntiRigidType(y)$
- **RA03 :**&ensp; $SemiRigidType(x) \land subClassOf(x,y) \rightarrow \neg AntiRigidType(y)$
- **RA04 :**&ensp; $x \neq y \land Kind(x) \land subClassOf(x,y) \rightarrow NonSortal(y)$
- **RA05 :**&ensp; $NonSortal(x) \land subClassOf(x,y) \rightarrow NonSortal(y)$
- **RA06 :**&ensp; $Phase(x) \land subClassOf(x,y) \rightarrow \neg Role(y) \land \neg RoleMixin(y)$
- **RA07 :**&ensp; $PhaseMixin(x) \land subClassOf(x,y) \rightarrow \neg RoleMixin(y)$

### UFO Some Rules Group

- **RS01 :**&ensp; $AntiRigidType(x) \land Sortal(x) \land Category(y) \land subClassOf(x,y) \rightarrow \exists z (RigidType(z) \land Sortal(z) \land subClassOf(x,z) \land subClassOf(z,y))$
- **RS02 :**&ensp; $Mixin(x) \rightarrow \exists y (subClassOf(y,x) \land AntiRigidType(y))$
- **RS03 :**&ensp; $Mixin(x) \rightarrow \exists y (subClassOf(y,x) \land RigidType(y))$
- **RS04 :**&ensp; $NonSortal(x) \rightarrow \exists y (Sortal(y) \land (subClassOf(y,x) \lor shareSuperClass(x,y)))$
- **RS05 :**&ensp; $NonSortal(x) \land Sortal(y) \land (subClassOf(y,x) \lor shareSuperClass(x,y)) \rightarrow \exists z (y \neq z \land Sortal(z) \land \neg shareKind(y,z) \land (subClassOf(z,x) \lor shareSuperClass(x,z)))$
- **RS06 :**&ensp; $Role(x) \land PhaseMixin(y) \land subClassOf(x,y) \rightarrow \exists z (Phase(z) \land subClassOf(x,z) \land subClassOf(z,y))$
- **RS07 :**&ensp; $Phase(x) \rightarrow \exists y (Phase (y) \land shareKind(x,y) \land \neg isSubClassOf(x,y) \land \neg isSubClassOf(y,x))$
- **RS08 :**&ensp; $PhaseMixin(x) \rightarrow \exists y (Category (y) \land isSubClassOf(x,y))$
- **RS09 :**&ensp; $PhaseMixin(x) \land Category(y) \land subClassOf(x,y) \rightarrow \exists z (PhaseMixin(z) \land \neg isSubClassOf(x,z) \land \neg isSubClassOf(z,x) \land isSubClassOf(z,y))$

### UFO Unique Rules Group

- **RU01 :**&ensp; $Sortal(x) \rightarrow \exists! y (subClassOf (x,y) \land Kind(y))$
