open util/relation

sig EndurantType {}
sig Sortal in EndurantType {}
sig NonSortal in EndurantType {}
sig RigidType in EndurantType {}
sig NonRigidType in EndurantType {}
sig SemiRigidType in NonRigidType {}
sig AntiRigidType in NonRigidType {}
one sig Kind, Subkind, Role, Phase, Category, RoleMixin, PhaseMixin, Mixin extends EndurantType {}

sig Class {
	subClassOf: set Class,
	type: one EndurantType
}

fun Kinds[] : Class {
	type.Kind
}

fun Subkinds[] : Class {
	type.Subkind
}

fun Phases[] : Class {
	type.Phase
}

fun Roles[] : Class {
	type.Role
}

fun Categories[] : Class {
	type.Category
}

fun RoleMixins[] : Class {
	type.RoleMixin
}

fun PhaseMixins[] : Class {
	type.PhaseMixin
}

fun Mixins[] : Class {
	type.Mixin
}

fun Sortals[] : Class {
	type.Sortal
}

fun NonSortals[] : Class {
	type.NonSortal
}

fun Rigids[] : Class {
	type.RigidType
}

fun AntiRigids[] : Class {
	type.AntiRigidType
}

fun RigidSortals[] : Class {
	Rigids & Sortals
}

fun AntiRigidSortals[] : Class {
	AntiRigids & Sortals
}

pred isRigid[x: Class] {
	x.type in RigidType
}

pred isAntiRigid[x: Class] {
	x.type in AntiRigidType
}

pred isSemiRigid[x: Class] {
	x.type in SemiRigidType
}

pred isNonSortal[x: Class] {
	x.type in NonSortal
}

pred isSortal[x: Class] {
	x.type in Sortal
}

pred isKind[x: Class] {
	x.type = Kind
}

pred isSubkind[x: Class] {
	x.type = Subkind
}

pred isPhase[x: Class] {
	x.type = Phase
}

pred isPhaseMixin[x: Class] {
	x.type = PhaseMixin
}

pred isRole[x: Class] {
	x.type = Role
}

pred isRoleMixin[x: Class] {
	x.type = RoleMixin
}
pred isCategory[x: Class] {
	x.type = Category
}

pred isMixin[x: Class] {
	x.type = Mixin
}

pred isSubClassOf[child: Class, parent: Class] {
	parent in child.subClassOf
}

// R29
pred shareKind[x: Class, y: Class] {
	one kind: Kinds | isSubClassOf[x, kind] and isSubClassOf[y, kind]
}

// R30
pred isSiblingOf[x: Class, y: Class] {
	some z: Class | isSubClassOf[x, z] and isSubClassOf[y, z]
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////	RULES
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

fact {
	// R01
	reflexive[subClassOf, Class]
	
	// R02
	transitive[subClassOf]

	// R03
	EndurantType = RigidType + NonRigidType
	disj[RigidType, NonRigidType]

	// R04
	NonRigidType = AntiRigidType + SemiRigidType 
	disj[AntiRigidType, SemiRigidType ]
	
	// R05
	EndurantType = Sortal + NonSortal
	disj[Sortal, NonSortal]

	// R06
	Kind in (RigidType & Sortal)
	
	// R07
	Subkind in (RigidType & Sortal)

	// R08
	disj[Kind, Subkind]

	// R09
	Role in (AntiRigidType & Sortal)

	// R10
	Phase in (AntiRigidType & Sortal)

	// R11
	disj[Role, Phase]

	// R12
	Category in (RigidType & NonSortal)

	// R13
	RoleMixin in (AntiRigidType & NonSortal)

	// R14
	PhaseMixin in (AntiRigidType & NonSortal)

	// R15
	disj[RoleMixin, PhaseMixin]

	// R16
	Mixin in (SemiRigidType & NonSortal)

	// R17
	RigidType in (Kind + Subkind + Category)

	// R18
	AntiRigidType in (Role + Phase + RoleMixin + PhaseMixin)
	
	// R19
	SemiRigidType in Mixin

	// R20
	Sortal in (Kind + Subkind + Role + Phase)

	// R21
	NonSortal in (Category + RoleMixin + PhaseMixin + Mixin)

	// R22: rigidTypesCannotSpecializeAntiRigidTypes
	all x,y: Class | isRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]

	// R23: semiRigidTypesCannotSpecializeAntiRigidTypes
	all x,y: Class | x!=y and isSemiRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]

	// R24: noAntiRigidSortalSpecializingCategoryDirectly 
	all x, y: Class | (isSubClassOf[x,y] and isAntiRigid[x] and isSortal[x] and isCategory[y]) implies 
							(some z: Class | isSubClassOf[x,z] and isSubClassOf[z,y] and isRigid[z] and isSortal[z])

	// R25: mixinsMustGeneralizeRigidAndAntiRigidTypes
	all x: Mixins | some y, z: Class | isSubClassOf[y,x] and isRigid[y] and isSubClassOf[z,x] and isAntiRigid[z] 

	// R26: kindsOnlySpecializeNonSortals
	all x,y: Class | x!=y and isKind[x] and isSubClassOf[x,y] implies isNonSortal[y]
	
	// R27: non-sortals only specialize non-sortals
	all x,y: Class | isNonSortal[x] and isSubClassOf[x,y] implies isNonSortal[y]

	// R28: every sortal specializes a unique kind
	all x: Class | isSortal[x] implies (one y: Class | isSubClassOf[x,y] and isKind[y])

	// R29 and R30 are implemented as predicates (see above)

	// R31: non-sortals do not have direct instances and classify individuals of at least two different kinds
	all x: NonSortals | 
		some disj y, z: Sortals | 
			( (isSubClassOf[y, x] or isSiblingOf[x, y]) and (isSubClassOf[z, x] or isSiblingOf[x, z]) and not shareKind[y, z])

	// R32: phases do not specialize roles and role-mixins 
	all x,y: Class | isPhase[x] and isSubClassOf[x,y] implies not isRole[y] and not isRoleMixin[y]

	// R33: phase-mixins do not specialize role-mixins
	all x,y: Class | isPhaseMixin[x] and isSubClassOf[x,y] implies not isRoleMixin[y]
	
	// R34: whenever a role specializes a phase mixin, it does that by specializing a phase that specializes that phase mixin
	all x, y: Class | (isRole[x] and isPhaseMixin[y] and isSubClassOf[x,y]) implies 
							(some z: Class | isPhase[z] and isSubClassOf[x,z] and isSubClassOf[z,y])

	// R35: phases come in sets 
	all x: Phases | some y: Phases | (shareKind[x, y] and not isSubClassOf[x,y] and not isSubClassOf[y,x])

	// R36: PhaseMixinsSpecializeCategories
	all x: PhaseMixins | some y: Categories | isSubClassOf[x,y]

	// R37: phaseMixinsSpecializationsMustBePartitions 
	all x: PhaseMixins | all y: Categories | isSubClassOf[x,y] implies (some z: PhaseMixins | (not isSubClassOf[x,z] and not isSubClassOf[z,x] and isSubClassOf[z,y]))
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////	CHECKS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


check kindCanOnlySpecializeCategoryAndMixin {
	all child, parent: Class | (child!=parent and isSubClassOf[child,parent] and isKind[child])
 		implies (isCategory[parent] or isMixin[parent])
} for 12

check subkindCanOnlySpecializeKindSubkindCategoryAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Subkind 
 		implies parent.type in (Kind + Subkind + Category + Mixin)
} for 12

check phaseCanOnlySpecializeKindSubkindPhaseCategoryPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Phase 
 							implies parent.type in (Kind + Subkind + Phase + Category + PhaseMixin + Mixin)
} for 12

check categoryCanOnlySpecializeCategoryAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Category 
 							implies parent.type in (Category + Mixin)
} for 12

check roleMixinCanOnlySpecializeCategoryRoleMixinPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and isRoleMixin[child] 
 							implies parent.type in (Category + RoleMixin + PhaseMixin + Mixin)
} for 12

check phaseMixinCanOnlySpecializeCategoryRoleMixinPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = PhaseMixin 
 							implies parent.type in (Category + PhaseMixin + Mixin)
} for 12


check mixinCanOnlySpecializeMixinAndCategory {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Mixin 
 							implies parent.type in (Mixin + Category)
} for 12



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////	RUNS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// NAMES STARTING WITH "NEGATIVE" MUST RESULT A "NO INSTANCE FOUND"

run RolesCanSpecializeRoles {
	some disj child, parent: Roles | isSubClassOf[child,parent]
} for 3

run RolesCanSpecializePhases {	
	some child: Roles | some parent: Phases | isSubClassOf[child,parent]
} for 4

run RolesCanSpecializeSubKinds {	
	some child: Roles | some parent: Subkinds | isSubClassOf[child,parent] 
} for 3

run RolesCanSpecializeKinds {	
	some child: Roles | some parent: Kinds | isSubClassOf[child,parent] 
} for 2

run RolesCanSpecializeRoleMixins {
	some child: Roles | some parent: RoleMixins | isSubClassOf[child,parent] 
} for 5

run RolesCanSpecializePhaseMixinsa {	
	some child: Roles | some parent: PhaseMixins | isSubClassOf[child,parent] 
} for 8

run RolesCanSpecializeCategories {	
	some child: Roles | some parent: Categories | isSubClassOf[child,parent] 
} for 4

run RolesCanSpecializeMixins {	
	some child: Roles | some parent: Mixins | isSubClassOf[child,parent] 
} for 4

run PhaseCanSpecializePhase {
	some disj child, parent: Phases | isSubClassOf[child,parent] 
} for 4

run PhaseMixinCanSpecializePhaseMixin {
	some disj child, parent: PhaseMixins | isSubClassOf[child,parent] 
} for 7

run NEGATIVEAntiRigidSortalCannotSpecializeCategoryWithoutAnIntermediateRigidSortal {
	some x, y: Class | (isRole[x] or isPhase[x]) and isCategory[y] and isSubClassOf[x,y] and (no z: Class | (isKind[z] or isSubkind[z]) and isSubClassOf[x,z] and isSubClassOf[z,y])
} for 12

run NEGATIVEnonSortalOccursWithASingleSortal{
	one Sortals and some NonSortals
} for 12

run NEGATIVEsinglePhase {
	some Kinds
	#Phases=1
} for 12

run NEGATIVEsinglePhaseMixin {
	some Categories
	#PhaseMixins=1
} for 12

run NEGATIVEPhase_MixinSpecializingRole_Mixin{
	some x, y: Class | (isPhase[x] or isPhaseMixin[x]) and (isRole[y] or isRoleMixin[y]) and isSubClassOf[x,y]
} for 12

run modelWithOneKindAndTwoPhases{
	#Kinds=1
	#Phases=2
} for 3

run modelWithOneSubkindAndTwoPhases{
	#Subkinds=1
	#Phases=2
	some disj x, y : Class | isPhase[x] and isSubkind[y] and isSubClassOf[x,y]
} for 4

run modelWithAllStereotypes{
	some Kinds
	some Subkinds
	some Roles
	some Phases
	some Categories
	some RoleMixins
	some PhaseMixins
	some Mixins
} for 12

