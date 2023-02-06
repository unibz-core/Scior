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

pred isBaseSortal[x: Class] {
	isSortal[x] and not isKind[x]
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

fact {
	transitive[subClassOf]
	reflexive[subClassOf, Class]
}

// R1
fact kindsCannotSpecializeSortals {
	all x,y: Class | x!=y and isKind[x] and isSubClassOf[x,y] implies isNonSortal[y]
}

// R2
fact  {
	all x,y: Class | x!=y and isNonSortal[x] and isSubClassOf[x,y] implies isNonSortal[y]
}

// R3
fact sortalsMustSpecializeUniqueKind {
	all x: Class | isBaseSortal[x] implies (one y: Class | x!=y and isSubClassOf[x,y] and isKind[y])
}

// R4
fact nonSortalMustHaveSortalSpecialization {
	all N: NonSortals | 
		some disj S1, S2: Sortals | 
			( (isSubClassOf[S1, N] or areSiblings[N+S1]) and (isSubClassOf[S2, N] or areSiblings[N+S2]) and not shareKind[S1+S2])
				
}

// R5
fact rigidTypesCannotSpecializeAntiRigidTypes {
	all x,y: Class | x!=y and isRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]
}

// R6
fact semiRigidTypesCannotSpecializeAntiRigidTypes {
	all x,y: Class | x!=y and isSemiRigid[x] and isSubClassOf[x,y] implies not isAntiRigid[y]
}

// R7
fact noAntiRigidSortalSpecializingCategoryDirectly {
	all a, c: Class | (isAntiRigid[a] and isSortal[a] and isCategory[c] and isSubClassOf[a,c]) implies (some r: Class | r!=a and isRigid[r] and isSortal[r] and isSubClassOf[a,r] and isSubClassOf[r,c])
}

// R8
fact mixinsMustGeneralizeRigidAndAntiRigidTypes {
	all m: Mixins | some x, y: Class | isSubClassOf[x,m] and isRigid[x] and isSubClassOf[y,m] and isAntiRigid[y] 
}

// R9
fact phasesCannotSpecializeRoles {
	all x,y: Class | x!=y and (isPhase[x] or isPhaseMixin[x]) and isSubClassOf[x,y] implies not (isRole[y] or isRoleMixin[y])
}

// R10
fact phasesComeInSets {
	all x: Phases | some y: Phases | (x!=y and areSiblings[x+y] and shareKind[x+y])
}

// R11
fact phaseMixinsComeInSets {
	all x: PhaseMixins | some y: PhaseMixins | (x!=y and areSiblings[x+y] and areSiblings[x+y])
}

// R12
fact noRoleDirectlySpecializingAPhaseMixin {
	all r, pm: Class | (isRole[r] and isPhaseMixin[pm] and isSubClassOf[r,pm]) implies (some p: Class | isPhase[p] and isSubClassOf[r,p] and isSubClassOf[p,pm])
}

check kindCanOnlySpecializeCategoryAndMixin {
	all child, parent: Class | (child!=parent and isSubClassOf[child,parent] and isKind[child])
 		implies (isCategory[parent] or isMixin[parent])
} for 5


check subkindCanOnlySpecializeKindSubkindCategoryAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Subkind 
 		implies parent.type in (Kind + Subkind + Category + Mixin)
} for 5


check phaseCanOnlySpecializeKindSubkindPhaseCategoryPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Phase 
 							implies parent.type in (Kind + Subkind + Phase + Category + PhaseMixin + Mixin)
} for 5

check categoryCanOnlySpecializeCategoryAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Category 
 							implies parent.type in (Category + Mixin)
} for 5

check roleMixinCanOnlySpecializeCategoryRoleMixinPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and isRoleMixin[child] 
 							implies parent.type in (Category + RoleMixin + PhaseMixin + Mixin)
} for 5

check phaseMixinCanOnlySpecializeCategoryRoleMixinPhaseMixinAndMixin {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = PhaseMixin 
 							implies parent.type in (Category + PhaseMixin + Mixin)
} for 5


check mixinCanOnlySpecializeMixinAndCategory {
	all child, parent: Class | child!=parent and isSubClassOf[child,parent] and child.type = Mixin 
 							implies parent.type in (Mixin + Category)
} for 5

run RolesCanSpecializeRoles {
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isRole[parent]
} for 5

run RolesCanSpecializePhases {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isPhase[parent]
} for 5

run RolesCanSpecializeSubKinds {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isSubkind[parent]
} for 5

run RolesCanSpecializeKinds {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isKind[parent]
} for 5

run RolesCanSpecializeRoleMixins {
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isRoleMixin[parent]
} for 5

run RolesCanSpecializePhaseMixins {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isPhaseMixin[parent]
} for 5

run RolesCanSpecializeCategories {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isCategory[parent]
} for 5

run RolesCanSpecializeMixins {	
	some child, parent: Class | child!=parent and isSubClassOf[child,parent] 
							and isRole[child] and isMixin[parent]
} for 5

run antiRigidSortalCannotSpecializeCategoryDirectly {
	#Kinds=2
	#AntiRigidSortals=1
	#Categories=1
	some r, c, k: Class | (isRole[r] or isPhase[r]) and isCategory[c] and (isKind[k] or isSubkind[k]) and isSubClassOf[r,c] and isSubClassOf[r,k] and not isSubClassOf[k,c]
} for 4

run nonSortalOccursWithASingleSortal{
	one Sortals and some NonSortals
} for 3

run {
	some Kinds
	some Subkinds
	some Roles
	some Phases
	some Categories
	some RoleMixins
	some PhaseMixins
	some Mixins
} for 12

run {
#Class > 4
} for 5






