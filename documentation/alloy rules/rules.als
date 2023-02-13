open util/relation

sig EndurantType {}
sig Sortal in EndurantType {}
sig NonSortal in EndurantType {}
sig RigidType in EndurantType {}
sig NonRigidType in EndurantType {}
sig SemiRigidType in NonRigidType {}
sig AntiRigidType in NonRigidType {}

one sig Kind, Subkind, Role, Phase, Category, RoleMixin, PhaseMixin, Mixin extends EndurantType {}

fact {
	EndurantType = Sortal + NonSortal
	EndurantType = RigidType + NonRigidType
	Kind + Subkind + Category = RigidType
	Role + Phase + RoleMixin + PhaseMixin = AntiRigidType
	Mixin = SemiRigidType
	Sortal = Kind + Subkind + Role + Phase
	NonSortal = Category + RoleMixin + PhaseMixin + Mixin
	NonRigidType = AntiRigidType + SemiRigidType 
}

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

pred areSiblings[Siblings: Class] {
	all child1, child2: Siblings | some parent: Class | isSubClassOf[child1, parent] and isSubClassOf[child2, parent]
}

pred shareKind[classes: Class] {
	all child1, child2: classes | one kind: Kinds | isSubClassOf[child1, kind] and isSubClassOf[child2, kind]
}

pred shareCategory[classes: Class] {
	all child1, child2: classes | some cat: Categories | isSubClassOf[child1, cat] and isSubClassOf[child2, cat]
}

fact {
	transitive[subClassOf]
	reflexive[subClassOf, Class]
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////	RULES
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



fact kindsCannotSpecializeSortals {
	all x,y: Class | x!=y and isKind[x] and isSubClassOf[x,y] implies isNonSortal[y]
}


fact  {
	all x,y: Class | isNonSortal[x] and isSubClassOf[x,y] implies isNonSortal[y]
}


fact sortalsMustSpecializeUniqueKind {
	all x: Class | isSortal[x] implies (one y: Class | isSubClassOf[x,y] and isKind[y])
}


fact nonSortalMustHaveSortalSpecialization {
	all N: NonSortals | 
		some disj S1, S2: Sortals | 
			( (isSubClassOf[S1, N] or areSiblings[N+S1]) and (isSubClassOf[S2, N] or areSiblings[N+S2]) and not shareKind[S1+S2])
				
}


fact rigidTypesCannotSpecializeAntiRigidTypes {
	all x,y: Class | isRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]
}


fact semiRigidTypesCannotSpecializeAntiRigidTypes {
	all x,y: Class | x!=y and isSemiRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]
}


fact noAntiRigidSortalSpecializingCategoryDirectly {
	all a, c: Class | (isAntiRigid[a] and isSortal[a] and isCategory[c] and isSubClassOf[a,c]) implies (some r: Class | isRigid[r] and isSortal[r] and isSubClassOf[a,r] and isSubClassOf[r,c])
}


fact mixinsMustGeneralizeRigidAndAntiRigidTypes {
	all m: Mixins | some x, y: Class | isSubClassOf[x,m] and isRigid[x] and isSubClassOf[y,m] and isAntiRigid[y] 
}


fact phasesCannotSpecializeRolesAndRoleMixins {
	all x,y: Class | isPhase[x] and isSubClassOf[x,y] implies not isRole[y] and not isRoleMixin[y]
}


fact phaseMixinsCannotSpecializeRoleMixins {
	all x,y: Class | isPhaseMixin[x] and isSubClassOf[x,y] implies not isRoleMixin[y]
}


fact noRoleDirectlySpecializingAPhaseMixin {
	all r, pm: Class | (isRole[r] and isPhaseMixin[pm] and isSubClassOf[r,pm]) implies (some p: Class | isPhase[p] and isSubClassOf[r,p] and isSubClassOf[p,pm])
}


fact phasesComeInSets {
	all x: Phases | some y: Phases | (not isSubClassOf[x,y] and not isSubClassOf[y,x] and shareKind[x+y])
}


fact phasesSpecializationsMustBePartitions {
	all disj x,y: Class | isPhase[x] and isSubClassOf[x,y] implies (some z: Class | (x!=z and y!=z and isPhase[z] and isSubClassOf[z,y]))
}


fact phaseMixinsComeInSets {
	all x: PhaseMixins | some y: PhaseMixins | (not isSubClassOf[x,y] and not isSubClassOf[y,x] and shareCategory[x+y])
}

fact phaseMixinsSpecializationsMustBePartitions {
	all x: PhaseMixins | all y: Categories | isSubClassOf[x,y] implies (some z: Class | (not isSubClassOf[x,z] and not not isSubClassOf[z,x] and isSubClassOf[z,y]))
}

fact PhaseMixinsSpecializeCategories{
	all x: PhaseMixins | some z: Categories | isSubClassOf[x,z]
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
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isRole[parent]
} for 12

run RolesCanSpecializePhases {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isPhase[parent]
} for 12

run RolesCanSpecializeSubKinds {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isSubkind[parent]
} for 12

run RolesCanSpecializeKinds {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isKind[parent]
} for 12

run RolesCanSpecializeRoleMixins {
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isRoleMixin[parent]
} for 12

run RolesCanSpecializePhaseMixinsViaIntermediatePhase {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isPhaseMixin[parent]
} for 12

run RolesCanSpecializeCategories {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isCategory[parent]
} for 12

run RolesCanSpecializeMixins {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isMixin[parent]
} for 12

run PhaseCanSpecializePhase {
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isPhase[child] and isPhase[parent]
} for 12

run PhaseMixinCanSpecializePhaseMixin {
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isPhaseMixin[child] and isPhaseMixin[parent]
} for 12

run AntiRigidSortalCanOnlySpecializeCategoryViaIntermediateRigidSortal {
	#Kinds=2
	#AntiRigidSortals=1
	#Categories=1
	some r, c, k: Class | (isRole[r] or isPhase[r]) and isCategory[c] and (isKind[k] or isSubkind[k]) and isSubClassOf[r,c] and isSubClassOf[r,k] and not isSubClassOf[k,c]
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

run modelWithSingleKindAndTwoPhases{
	#Kinds=1
	#Phases=2
} for 12

run modelWithSingleSubkindAndTwoPhases{
	#Subkinds=1
	#Phases=2
	some disj x, y : Class | isPhase[x] and isSubkind[y] and isSubClassOf[x,y]
} for 12

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
