# OntCatOWL: Implemented Reasoning Rules

This document describes all the rules implemented in OntCatOWL.

## Content

- [Scope](#scope)
- [Descriptions](#descriptions)
- [Implemented Rules](#implemented-rules)
  - [Rule k_s_sup](#rule-k_s_sup)
  - [Rule s_k_sub](#rule-s_k_sub)
  - [Rule t_k_sup](#rule-t_k_sup)
  - [Rule ns_s_sup](#rule-ns_s_sup)
  - [Rule s_ns_sub](#rule-s_ns_sub)
  - [Rule r_ar_sup](#rule-r_ar_sup)
  - [Rule ar_r_sub](#rule-ar_r_sub)
  - [Rule n_r_t](#rule-n_r_t)
  - [Rule ns_s_spe](#rule-ns_s_spe)
  - [Rule nk_k_sup](#rule-nk_k_sup)
  - [Rule s_nsup_k](#rule-s_nsup_k)
  - [Rule ns_sub_r](#rule-ns_sub_r)
  - [Rule nrs_ns_r](#rule-nrs_ns_r)
  - [Rule ks_sf_in](#rule-ks_sf_in)
  - [Rule sub_r_r](#rule-sub_r_r)
- [References](#references)

## Scope

The current version of the OntCatOWL is limited to Endurant types. I.e., there are no rules implemented for other
ontological categories provided by [the Unified Foundational Ontology (UFO)](https://philpapers.org/archive/PORUUF.pdf).
Even though gUFO has two taxonomies (one with classes whose instances are individuals and another with classes whose
instances are types), because of this restriction, only the latter is handled by the rules here presented—more
specifically, OntCatOWL uses the [Endurant types](https://nemo-ufes.github.io/gufo/#enduranttypes) part of the types
hierarchy. This hierarchy addresses two ontological meta-properties of
entities: [sortality](https://ontouml.readthedocs.io/en/latest/theory/identity.html) (related to the *identity
principle* the entity may provide or carry)
and [rigidity](https://ontouml.readthedocs.io/en/latest/theory/rigidity.html).

## Descriptions

In the next section, we describe the fifteen rules implemented in the OntCatOWL.

Regarding the rigidity and sortality meta-properties, the rules implemented in OntCatOWL were originally defined for
OntoUML (first in [1], later in [2]) and, hence, we had to convert them from the diagrammatical modeling language (
OntoUML) reality to the RDF-based semantic web paradigm, in which gUFO lies.

During the development of this work, we could identify UFO constraints that were absent from the mentioned reference
works. We implemented in OntCatOWL new rules for phase partitions and for subtypes of roles to cover all necessary
constraints.

The implementation of the set of rules present in OntCatOWL is the first one done for gUFO and, hence, is an important
contribution to its related community.

In the next section, we describe the OntCatOWL rules using four items:

- **Rule:** A description of the rule that is implemented.
- **Reason:** A description of the rule’s existence reason according to UFO.
- **Description:** A description of the rule focused on how it was implemented.
- **Behavior:** A description of the different actions that the rule may trigger in the model.

Regarding the rule’s **behavior**, we always have three possibilities, which are represented using the following
acronyms:

- **US**: User can set the class type or skip.
- **SA**: Automatically set all.
- **RI**: Report incompleteness.

Every time a rule is triggered, a new type is positively (e.g., the class “Person” is set as a “gufo:Kind”) or
negatively (e.g., “Person” is set as not a “gufo:Role”) asserted to a class. A unique string code in the
format *`x_y_z`* identifies every implemented rule.

## Implemented Rules

### Rule k_s_sup

- **Rule:** A `gufo:Kind` cannot have `gufo:Sortals` as its direct or indirect supertypes.
  - Code: *k_s_sup*
- **Reason:** Every Sortal must have exactly one identity principle.
- **Description:** When this rule identifies a class categorized as `gufo:Kind`, it identifies all its supertypes and
  sets them as not `gufo:Sortal`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule s_k_sub

- **Rule:** `gufo:Sortals` cannot have a `gufo:Kind` as direct or indirect subtypes.
  - Code: s_k_sub
- **Reason:** Every Sortal must have exactly one identity principle.
- **Description:** When this rule identifies a class categorized as `gufo:Sortal`, it identifies all its subtypes and
  sets them as not `gufo:Kind`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule t_k_sup

- **Rule:** A type cannot have more than one `gufo:Kind` as its direct or indirect supertypes.
  - Code: t_k_sup
- **Reason:** Every Sortal must have exactly one identity principle.
- **Description:** Identifies a `gufo:Kind`. With the exception for the `gufo:Kind` itself, all direct and indirect
  superclasses of all subclasses of this `gufo:Kind` are set as not `gufo:Kinds`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule ns_s_sup

- **Rule:** A `gufo:NonSortal` cannot have a `gufo:Sortal` as its direct or indirect supertype.
  - Code: ns_s_sup
- **Reason:** Non-Sortals aggregate identities from at least two different identity principles providers.
- **Description:** For each `gufo:NonSortal` class identified, sets all its direct and indirect superclasses as
  not `gufo:Sortals`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule s_ns_sub

- **Rule:** A `gufo:Sortal` cannot have a `gufo:NonSortal` as its direct or indirect subtype.
  - Code: s_ns_sub
- **Reason:** Every Sortal must have exactly one identity principle.
- **Description:** For each `gufo:Sortal` class identified, set all its direct and indirect subclasses as
  not `gufo:NonSortal`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule r_ar_sup

- **Rule:** A `gufo:Rigid` or a `gufo:SemiRigid` type cannot have a `gufo:AntiRigid` type as its direct or indirect
  supertypes.
  - Code: r_ar_sup
- **Reason:** Rigid types cannot specialize Anti-Rigid types.
- **Description:** For each `gufo:Rigid` or `gufo:SemiRigid` class identified, sets all its direct and indirect
  superclasses as not `gufo:AntiRigid`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule ar_r_sub

- **Rule:** A `gufo:AntiRigid` type cannot have a `gufo:Rigid` or `gufo:SemiRigid` type as its direct or indirect
  subtypes.
  - Code: ar_r_sub
- **Reason:** Rigid types cannot specialize Anti-Rigid types.
- **Description:** For each `gufo:AntiRigid` class identified, sets all its direct and indirect subclasses as
  not `gufo:Rigid` and as not `gufo:SemiRigid`.
- **Behavior:**
  - Automation: Same execution for both complete and incomplete models.
  - Completeness: Automatic rule. Interaction is not needed in any case.

### Rule n_r_t

- **Rule:** In complete models, every type without supertypes and without subtypes must be a `gufo:Kind`.
  - Code: n_r_t
- **Reason:** Every type must supply (Kinds) or carry (Non-Kind Sortals) a single identity principle or aggregate (
  Non-Sortals) multiple identity principles.
- **Description:** If a class is not a `gufo:Kind` and if it is a root and a leaf node at the same time (i.e., an
  isolated class), then perform action.
- **Behavior:**
  - Complete models: Set as `gufo:Kind`.
  - Incomplete & Automatic models: Report incompleteness.
  - Incomplete & Interactive models: User can set as `gufo:Kind` or skip.

### Rule ns_s_spe

- **Rule:** Given a `gufo:NonSortal` N, there must be at least two `gufo:Sortals` S1 and S2 with different identity
  principles (i.e., that are specializations of different `gufo:Kinds`) that:
  - directly or indirectly specializes N, **or** that
  - directly or indirectly specializes:
    1. a supertype of N **or**
    2. a supertype of one of the subtypes of N.

In other words, from any `gufo:NonSortal`, at least two `gufo:Kinds` must be reachable by navigating its
generalization/specialization relations. Code: ns_s_spe.

- **Reason:** Non-Sortals aggregate identities from at least two different identity principles providers.
- **Behavior:** Considering P the number of possibilities and N the necessary number (N>0):
  - If N <= 0: do nothing.
  - **Regarding possible actions:**
    - RI when P<=0 or N+A or (C+A and P>N)
    - SA when P>0 and (C and P<=N)
    - US when P>0 and (N+I or (C+I and P>N))
  - **Regarding possible configurations:**
    - Complete & Automatic:
      - RI when P<=0 or when (P>0 and P>N)
      - SA when (P>0 and P<=N)
    - Complete & Interactive:
      - RI when P<=0
      - US when (P>0 and P>N)
      - SA when (P>0 and P<=N)
    - Incomplete & Automatic:
      - RI (always)
    - Incomplete & Interactive:
      - RI when P<=0
      - US when P>0

### Rule nk_k_sup

- **Rule:** Every `gufo:Sortal` that is not a `gufo:Kind` must have exactly one `gufo:Kind` as a direct or indirect
  supertype.
  - Code: nk_k_sup
- **Reason:** Every Sortal must have exactly one identity principle.
- **Behavior:** Only executed if no direct or indirect supertype is classified as a `gufo:Kind`. Considering P the
  number of directly or indirectly related supertypes that can be `gufo:Kinds`.
  - **Regarding possible actions:**
    - RI: P=0 or N+A or (P>1 and C+A)
    - SA: P=1 and C
    - US: (P=1 and N+I) or (P>1 and I)
  - **Regarding possible configurations:**
    - Complete & Automatic:
      - RI when P=0 or when P>1
      - SA when P=1
    - Complete & Interactive:
      - RI when P=0
      - SA when P=1
      - US when P>1
    - Incomplete & Automatic:
      - RI (always)
    - Incomplete & Interactive:
      - RI when P=0
      - US when P>=1
  - **Regarding the number of possibilities (P):**
    - **P=0:** always RI
    - **P=1:** (SA when Complete) or (RI when incomplete & Automatic) or (US when incomplete & Interactive)
    - **P>1:** (RI when Automatic) or (US when Interactive)

### Rule s_nsup_k

- **Rule:** In complete models, every `gufo:Sortal` without supertypes is a `gufo:Kind`.
  - Code: s_nsup_k
- **Reason:** Every Sortal must have exactly one identity principle, which is provided by a Kind.
- **Behavior:**
  - Complete (Automatic or Interactive): Set as `gufo:Kind`.
  - Incomplete & Automatic: Report incompleteness.
  - Incomplete & Interactive: User can set as `gufo:Kind`.

### Rule ns_sub_r

- **Rule:** In complete models, `gufo:NonSortals` with only `gufo:Rigid` direct subtypes are always `gufo:Categories`.
  - Code: ns_sub_r
- **Reason:** Rigid types cannot specialize Anti-Rigid types.
- **Behavior:**
  - Complete models (Automatic or Interactive): Set as `gufo:Category`.
  - Incomplete models (Automatic or Interactive): Not executed.

### Rule nrs_ns_r

- **Rule:** In complete models, `gufo:NonRigid` that are `gufo:Sortals` with no sibling classes are always `gufo:Roles`.
  - Code: nrs_ns_r
- **Reason:** Phases always occur in phase partitions.
- **Behavior:**
  - Complete (Automatic or Interactive): If can be a `gufo:Role`, set as `gufo:Role`. If cannot, report incompleteness.
  - Incomplete & Automatic: Report incompleteness.
  - Incomplete & Interactive: Ask the user if she/he should be set to `gufo:Role`. If not, report incompleteness.

### Rule ks_sf_in

- **Rule:** For every class classified as a `gufo:Phase`, there is an incompleteness if the `gufo:Phase` has no sibling
  classes or if all its siblings are `gufo:NonSortals` or `gufo:RigidTypes`.
  - Code: ks_sf_in
- **Reason:** Phases always occur in phase partitions.
- **Behavior:** Report incompleteness in all cases.

### Rule sub_r_r

- **Rule:** Every direct or indirect specialization of a `gufo:Role` is also a `gufo:Role`.
  - Code: sub_r_r
- **Reason:** Roles are Anti-Rigid and relationally dependent Sortals.
- **Description:** `gufo:Phases` are relationally independent types. `gufo:Roles` are relationally dependent types. As
  all specializations of relationally dependent types are also relationally dependent, they must be `gufo:Roles` and
  cannot be `gufo:Phases`. Every specialization of a `gufo:Role` also depends on the relation that their supertype has.
- **Behavior:** In all cases, set as `gufo:Role`.

## References

**[1]** Guizzardi, G., Fonseca, C. M., Benevides, A. B., Almeida, J. P. A., Porello, D., & Sales, T. P. (2018)
. [Endurant Types in Ontology-Driven Conceptual Modeling: Towards OntoUML 2.0](https://link.springer.com/chapter/10.1007/978-3-030-00847-5_12)
. In J. C. Trujillo, K. C. Davis, X. Du, Z. Li, T. W. Ling, G. Li, & M. L. Lee (Eds.), Conceptual Modeling (pp. 136–150)
. Cham: Springer International Publishing. [(download here)](https://philarchive.org/archive/PORETI)

**[2]** Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021)
. [Types and taxonomic structures in conceptual modeling: A novel ontological theory and engineering support](https://www.sciencedirect.com/science/article/pii/S0169023X21000185?casa_token=dXmMN1JNCLkAAAAA:OvdFW1ZDuUzhTut2YW4fcqk1uT7-QPeSzfNsU2bBwYdfyKIPxege4VVgwyNg4xPBbV7o4vJyTSz0)
. Data & Knowledge Engineering, 134, 101891. doi:
10.1016/j.datak.2021.101891 [(download here)](http://www.inf.ufes.br/~gguizzardi/Types_and_Taxonomic_Structures_in_Conceptual_Modeling:A%20Novel_Ontological_Theory_and_Engineering_Support.pdf)
