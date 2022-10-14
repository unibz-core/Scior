""" Complementary functions for implementing types rules with a reduced complexity. """


def treat_rule(ontology_dataclass, configurations):
    # Case kind in NOT, not treated! Verify!
    if gufo_kind in ontology_dataclass.can_type:
        if configurations["is_complete"]:
            ontology_dataclass.move_element_to_is_list(gufo_kind)
        elif configurations["automation_level"] != "automatic_only":
            # TODO (@pedropaulofb): Implement!
            user_interaction_rule_n_r_t(ontology_dataclass)
        # Case incomplete and automatic_only
        else:
            logger.warning(f"Deficiency detected but not treated. "
                           f"Class {ontology_dataclass.uri} does not have known superclasses and "
                           f"subclasses and does not have an identity provider.")
    # If gufo_kind in ontology_dataclass.not_type
    else:
        logger.warning(f"Cannot set class {ontology_dataclass.uri} as {gufo_kind}. "
                       f"Inconsistency detected. Program aborted.")
        exit(1)
