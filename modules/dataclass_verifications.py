""" Module with functions for verifying the consistency of the dataclasses """

if __name__ != "__main__":

    import logging

    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


    def has_duplicates(list):
        """ Check if given list contains any duplicated element """
        if len(list) == len(set(list)):
            return False
        else:
            return True


    def check_duplicated_same_list_ontology(ontology_class):
        """ Verifies if there are duplicated elements in each one of the OWLClass lists"""
        duplicated_list = []

        if has_duplicates(ontology_class.is_type):
            duplicated_list.append("is_type")
        elif has_duplicates(ontology_class.is_individual):
            duplicated_list.append("is_individual")
        elif has_duplicates(ontology_class.can_type):
            duplicated_list.append("can_type")
        elif has_duplicates(ontology_class.can_individual):
            duplicated_list.append("can_individual")
        elif has_duplicates(ontology_class.not_type):
            duplicated_list.append("not_type")
        elif has_duplicates(ontology_class.not_individual):
            duplicated_list.append("not_individual")

        if len(duplicated_list) != 0:
            logging.error(
                f"INCONSISTENCY DETECTED: Same element in two lists for element {ontology_class.name} in list {duplicated_list} in {__name__}.")
            exit(1)
        else:
            logging.debug(f"No inconsistency detected in {ontology_class.name} in {__name__}.")

            # There is no need for a return because the errors area already displayed case detected.


    def check_duplicated_same_list_gufo(gufo_class):
        """ Verifies if there are duplicated elements in each one of the GUFOClass lists"""
        duplicated_list = []

        if has_duplicates(gufo_class.is_list):
            duplicated_list.append("is_list")
        elif has_duplicates(gufo_class.can_list):
            duplicated_list.append("can_list")
        elif has_duplicates(gufo_class.can_type):
            duplicated_list.append("not_list")

        if len(duplicated_list) != 0:
            logging.error(
                f"INCONSISTENCY DETECTED: Same element in two lists for element {gufo_class.name} in list {duplicated_list} in {__name__}.")
            exit(1)
        else:
            logging.debug(f"No inconsistency detected in {gufo_class.name} in {__name__}.")

        # There is no need for a return because the errors area already displayed case detected.


    def correct_number_of_elements_ontology(dataclass, expected_number):
        """ Sum of elements from all the lists in a dataclass must be equal to expected_number """

        total_length = len(dataclass.is_type) + len(dataclass.is_individual) + len(dataclass.can_type) + len(
            dataclass.can_individual) + len(dataclass.not_type) + len(dataclass.not_individual)

        if total_length != expected_number:
            logging.error(
                f"INCONSISTENCY DETECTED: The number of elements in {dataclass.name} is {total_length}, which is different from the expected number ({expected_number}) in {__name__}.")
            exit(1)
        else:
            logging.debug(f"No inconsistency detected in {dataclass.name} in {__name__}.")


    def correct_number_of_elements_gufo(dataclass, expected_number):
        """Sum of elements from all the lists in a dataclass must be equal to expeted_number"""

        total_length = len(dataclass.is_list) + len(dataclass.can_list) + len(dataclass.not_list)

        if total_length != expected_number:
            logging.error(
                f"INCONSISTENCY DETECTED: The number of elements in {dataclass.name} is {total_length}, which is different from the expected number ({expected_number}) in {__name__}.")
            exit(1)
        else:
            logging.debug(f"No inconsistency detected in {dataclass.name} in {__name__}.")


def duplicated_other_list(list1, list2):
    """ Returns a boolean indicating if the value of one list appears in another """

    check_1in2 = any(item in list1 for item in list2)
    check_2in1 = any(item in list2 for item in list1)
    result = check_1in2 or check_2in1

    return result


def duplicated_other_list_ontology(ontology_dataclass):
    """ No same string must be in two lists at the same time. """

    duplicated_list = []

    if duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.is_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.can_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.not_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.is_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.can_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.not_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.is_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.can_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.not_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.can_type):
        duplicated_list.append("is_type")
        duplicated_list.append("can_type")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.not_type):
        duplicated_list.append("is_type")
        duplicated_list.append("not_type")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.not_type):
        duplicated_list.append("can_type")
        duplicated_list.append("not_type")
    elif duplicated_other_list(ontology_dataclass.is_individual, ontology_dataclass.can_individual):
        duplicated_list.append("is_individual")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.is_individual, ontology_dataclass.not_individual):
        duplicated_list.append("is_individual")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.can_individual, ontology_dataclass.not_individual):
        duplicated_list.append("can_individual")
        duplicated_list.append("not_individual")

    if len(duplicated_list) != 0:
        logging.error(
            f"INCONSISTENCY DETECTED: Same element in two lists for element {ontology_dataclass.name} in {__name__}. Lists {duplicated_list[0]} and {duplicated_list[1]}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {ontology_dataclass.name} in {__name__}. ")

    # There is no need for a return because the errors area already displayed case detected.


def duplicated_other_list_gufo(gufo_dataclass):
    """ No same string must be in two lists at the same time."""
    duplicated_list = []

    if duplicated_other_list(gufo_dataclass.is_list, gufo_dataclass.can_list):
        duplicated_list.append("is_list")
        duplicated_list.append("can_list")
    elif duplicated_other_list(gufo_dataclass.is_list, gufo_dataclass.not_list):
        duplicated_list.append("is_list")
        duplicated_list.append("not_list")
    elif duplicated_other_list(gufo_dataclass.can_list, gufo_dataclass.not_list):
        duplicated_list.append("can_list")
        duplicated_list.append("not_list")

    if len(duplicated_list) != 0:
        logging.error(
            f"INCONSISTENCY DETECTED: Same element in two lists for element {gufo_dataclass.name} in {__name__}. Lists {duplicated_list[0]} and {duplicated_list[1]}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {gufo_dataclass.name} in {__name__}. ")

    # There is no need for a return because the errors area already displayed case detected.
