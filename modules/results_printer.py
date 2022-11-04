""" Fucntions for printing statistics to the user. """
from prettytable import PrettyTable, SINGLE_BORDER

from modules.logger_config import initialize_logger

# Global values
CL = " Classes "
TU = "Totally Unknown"
PK = "Partially Known"
TK = " Totally Known "


def print_statistics_screen(list_values, restriction="PRINT_ALL"):
    """ Receives lists of before and after values and prints them in a table.

    Restrictions:
        - "PRINT_ALL" - prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    list_values positions:

        list[0] = len(statistics_list)

        list[1] = totally_unknown_types
        list[2] = totally_unknown_individuals
        list[3] = totally_unknown_all

        list[4] = partially_known_types
        list[5] = partially_known_individuals
        list[6] = partially_known_all

        list[7] = totally_known_types
        list[8] = totally_known_individuals
        list[9] = totally_known_all
    """

    logger = initialize_logger()

    if list_values[0] != list_values[10]:
        logger.error("Number of classes must be the same before and after the software execution. Program aborted.")
        exit(1)

    print("\n##### FINAL ONTCATOWL CLASSIFICATION SUMMARY #####")

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        # Printing TYPES

        print(f"\nOntCatOWL results the evaluation of TYPES in {list_values[0]} classes:")
        table_types = PrettyTable(["Situation", CL, TU, PK, TK])

        table_types.add_row(["Before", list_values[0], list_values[1], list_values[4], list_values[7]])
        table_types.add_row(["After", list_values[10], list_values[11], list_values[14], list_values[17]])

        table_types.align = "c"
        table_types.set_style(SINGLE_BORDER)

        print(table_types)
        print()

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        # Printing INDIVIDUALS

        print(f"\nOntCatOWL results the evaluation of INDIVIDUALS in {list_values[0]} classes:")
        table_individuals = PrettyTable(["Situation", CL, TU, PK, TK])

        table_individuals.add_row(["Before", list_values[0], list_values[2], list_values[5], list_values[8]])
        table_individuals.add_row(["After", list_values[10], list_values[12], list_values[15], list_values[18]])

        table_individuals.align = "c"
        table_individuals.set_style(SINGLE_BORDER)

        print(table_individuals)
        print()

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        # Printing TOTAL

        print(f"\nOntCatOWL results the evaluation of TYPES and INDIVIDUALS in {list_values[0]} classes:")
        table_total = PrettyTable(["Situation", CL, TU, PK, TK])

        table_total.add_row(["Before", list_values[0], list_values[3], list_values[6], list_values[9]])
        table_total.add_row(["After", list_values[10], list_values[13], list_values[16], list_values[19]])

        table_total.align = "c"
        table_total.set_style(SINGLE_BORDER)

        print(table_total)
        print()
