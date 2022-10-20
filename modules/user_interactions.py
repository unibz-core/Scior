""" Generic functions used for user interaction. """
from prettytable import PrettyTable

from modules.logger_config import initialize_logger
from modules.utils_dataclass import get_element_list


def select_class_from_list(list_ontology_dataclasses, list_option_classes):
    """ The user can select one class from the list of classes received as parameter. Returns the URI of the class. """

    list_option_classes.sort()

    # TODO (@pedropaulofb): Treat case where selection_list size = 0

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


def set_type_for_class(list_ontology_dataclasses, class_name):
    """ The user can set a type for the class received as parameter. """
    logger = initialize_logger()

    # remember skip option

    number_of_options = 0
    found = False

    print(f"The current status of class {class_name} is:")

    for ontology_dataclass in list_ontology_dataclasses:
        if ontology_dataclass.uri == class_name:
            print(f"\tIS: {ontology_dataclass.is_type}")
            print(f"\tCAN: {ontology_dataclass.can_type}")
            print(f"\tNOT: {ontology_dataclass.not_type}")
            number_of_options = len(ontology_dataclass.can_type)
            found = True
            break

    if not found:
        logger.error("Unknown class. Program aborted.")
        exit(1)

    if number_of_options == 0:
        print("Class types are already known. No options are available.")
        return "nok"

    # user chose to set IS or NOT
    # print CAN options
    # user select option
    # move option to selected list
    pass
