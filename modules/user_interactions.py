""" Generic functions used for user interaction. """
from prettytable import PrettyTable

from modules.logger_config import initialize_logger
from modules.utils_dataclass import get_element_list, select_list


def print_class_types(ontology_dataclass):
    """ Print current status of a dataclass (internal lists). """

    print(f"The current status of the class {ontology_dataclass.uri} is:")
    print(f"\t- IS\t: {ontology_dataclass.is_type}")
    print(f"\t- CAN\t: {ontology_dataclass.can_type}")
    print(f"\t- NOT\t: {ontology_dataclass.not_type}")


def print_list_classes_and_types(list_ontology_dataclasses, list_option_classes):
    """ Prints table with all possible classes to be selected and its known types. """

    table = PrettyTable(['ID', 'URI', 'Known IS Types', "Known CAN Types", "Known NOT Types"])

    node_id = 0
    for ontology_class in list_option_classes:
        node_id += 1
        class_is_types = get_element_list(list_ontology_dataclasses, ontology_class, "is_type")
        class_can_types = get_element_list(list_ontology_dataclasses, ontology_class, "can_type")
        class_not_types = get_element_list(list_ontology_dataclasses, ontology_class, "not_type")
        table.add_row([node_id, ontology_class, class_is_types,
                       class_can_types, class_not_types])

    table.align = "l"
    print(table)


def select_class_from_list(list_ontology_dataclasses, list_option_classes):
    """ The user can select one class from the list of classes received as parameter. Returns the URI of the class.
    Return values can be: the URI of the selected class (string) or "skipped".
    """

    logger = initialize_logger()

    list_option_classes.sort()

    if len(list_option_classes) == 0:
        logger.error("List of options is empty. Situation must be treated before function call. Program aborted.")
        exit(1)

    print_list_classes_and_types(list_ontology_dataclasses, list_option_classes)

    selected_id = input("Enter the ID of the class to be selected or enter 0 to skip the selection: ")
    selected_id.strip()
    selected_id = int(selected_id)

    if selected_id > 0:
        selected_class = list_option_classes[selected_id - 1]
        print(f"The chosen class was: {selected_class}")

    else:
        selected_class = "skipped"
        print("Selection skipped. No class selected.")

    return selected_class


def set_type_for_class(ontology_dataclass):
    """ The user can set a type for the class received as parameter.
    Possible return values are: ok (valid situations: correct selection or skip option), nok (invalid situations).

    When dataclass is not known (i.e., only name is known), use the follwoing before calling this function:
        ontology_dataclass = return_dataclass_from_class_name(list_ontology_dataclasses, class_name)
    """

    logger = initialize_logger()

    print_class_types(ontology_dataclass)
    print("\n")

    number_of_options = len(ontology_dataclass.can_type)

    # INVALID situation treatment
    if number_of_options == 0:
        print("Class types are already known. No options are available.")
        return "nok"

    # VALID situation treatment
    table = PrettyTable(['ID', "CAN Type"])

    node_id = 0
    for can_type in ontology_dataclass.can_type:
        node_id += 1
        table.add_row([node_id, can_type])

    table.align = "l"
    print(table)
    print("\n")

    selected_id = input("Enter the ID of the type to be selected or enter 0 to skip the selection: ")
    selected_id.strip()
    selected_id = int(selected_id)

    if selected_id > 0:
        selected_type = ontology_dataclass.can_type[selected_id - 1]
        print(f"The chosen type was: {selected_type}")
    else:
        print("Selection skipped. No type selected.")
        return "ok"

    selected_list = select_list(["is", "not"])

    if selected_list == "is":
        ontology_dataclass.move_element_to_is_list(selected_type)
    else:
        ontology_dataclass.move_element_to_not_list(selected_type)

    logger.debug(f"For class {ontology_dataclass.uri}, type {selected_type} successfully moved to {selected_list} list")
    return "ok"