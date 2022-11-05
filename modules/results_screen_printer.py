""" Fucntions for printing statistics to the user. """
from prettytable import PrettyTable, SINGLE_BORDER

from modules.logger_config import initialize_logger

# Global values
CL = "Classes Total"
TU = "Totally Unknown"
PK = "Partially Known"
TK = "Totally Known"


def print_statistics_screen(list_values_classes, list_values_classifications, restriction="PRINT_ALL"):
    """ Receives lists of before and after values and prints them in a table.

    Restrictions:
        - "PRINT_ALL" - prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    list_values positions:

        FOR NUMBERS OF CLASSES:
            return_list_classes[0] = total_classes_number

            return_list_classes[1] = totally_unknown_classes_types
            return_list_classes[2] = totally_unknown_classes_individuals
            return_list_classes[3] = totally_unknown_classes_all

            return_list_classes[4] = partially_known_classes_types
            return_list_classes[5] = partially_known_classes_individuals
            return_list_classes[6] = partially_known_classes_all

            return_list_classes[7] = totally_known_classes_types
            return_list_classes[8] = totally_known_classes_individuals
            return_list_classes[9] = totally_known_classes_all

        FOR NUMBERS OF CLASSIFICATIONS:
            return_list_classifications[0] = total_classifications_number

            return_list_classifications[1] = total_classifications_types
            return_list_classifications[2] = total_classifications_individuals

            return_list_classifications[3] = number_unknown_classifications_types
            return_list_classifications[4] = number_known_classifications_types

            return_list_classifications[5] = number_unknown_classifications_individuals
            return_list_classifications[6] = number_known_classifications_individuals

            return_list_classifications[7] = number_unknown_classifications_total
            return_list_classifications[8] = number_known_classifications_total
    """

    logger = initialize_logger()

    if list_values_classes[0] != list_values_classes[10]:
        logger.error("Number of classes must be the same before and after the software execution. Program aborted.")
        exit(1)

    print("\n##### FINAL ONTCATOWL CLASSIFICATION SUMMARY #####")

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        # Printing TYPES

        print(f"\nResults of OntCatOWL execution when evaluating TYPES for {list_values_classes[0]} classes:")
        table_types = PrettyTable(["Evaluation", "Before", "After"])

        table_types.add_row([CL, list_values_classes[0], list_values_classes[10]])
        table_types.add_row([TU, list_values_classes[1], list_values_classes[11]])
        table_types.add_row([PK, list_values_classes[4], list_values_classes[14]])
        table_types.add_row([TK, list_values_classes[7], list_values_classes[17]])

        table_types.align = "c"
        table_types.align["Evaluation"] = "l"
        table_types.set_style(SINGLE_BORDER)

        print(table_types)
        print()

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        # Printing INDIVIDUALS

        print(f"\nResults of OntCatOWL execution when evaluating INDIVIDUALS for {list_values_classes[0]} classes:")
        table_individuals = PrettyTable(["Evaluation", "Before", "After"])

        table_individuals.add_row([CL, list_values_classes[0], list_values_classes[10]])
        table_individuals.add_row([TU, list_values_classes[2], list_values_classes[12]])
        table_individuals.add_row([PK, list_values_classes[5], list_values_classes[15]])
        table_individuals.add_row([TK, list_values_classes[8], list_values_classes[18]])

        table_individuals.align = "c"
        table_individuals.align["Evaluation"] = "l"
        table_individuals.set_style(SINGLE_BORDER)

        print(table_individuals)
        print()

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        # Printing TOTAL

        print(
            f"\nResults of OntCatOWL execution when evaluating TYPES and INDIVIDUALS for {list_values_classes[0]} classes:")
        table_total = PrettyTable(["Evaluation", "Before", "After"])

        table_total.add_row([CL, list_values_classes[0], list_values_classes[10]])
        table_total.add_row([TU, list_values_classes[3], list_values_classes[13]])
        table_total.add_row([PK, list_values_classes[6], list_values_classes[16]])
        table_total.add_row([TK, list_values_classes[9], list_values_classes[19]])

        table_total.align = "c"
        table_total.align["Evaluation"] = "l"
        table_total.set_style(SINGLE_BORDER)

        print(table_total)
        print()
