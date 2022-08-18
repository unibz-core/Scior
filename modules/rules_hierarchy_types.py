""" Rules applied to the TYPES HIERARCHY. """

### SCOPE

# multi-level not treated, hence every class must INSTANTIATE a single class in the type hierarchy.
# Endurants only.

### General rules.

# Every element must instantiate a single class of the types' hierarchy.

### Rules about SORTALITY of elements.

# Every entity must have an identity or aggregate identities.
# A single entity cannot have two identity providers. E.g., any entity can specialize two different gufo:Kind classes.

# RULE: Kinds, as identity providers, cannot have another Sortal (elements that carry or provide identity) as its direct or indirect supertype.
# CONS1: Direct or indirect superclasses of a class that instantiates gufo:Kind cannot be of type gufo:Sortal (and, consequently, of its subtypes).
# CONS2: Direct or indirect superclasses of a class that instantiates gufo:Kind must be of type gufo:NonSortal.

### Rules about RIGIDIY of elements.

# Non-rigid classes cannot specialize rigid classes.
