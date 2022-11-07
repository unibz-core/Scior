""" Fucntions for printing statistics to the user. """
from prettytable import PrettyTable, SINGLE_BORDER

from modules.logger_config import initialize_logger


def generate_classes_table_to_be_printed(list_values_classes, table_option, border_option):
    """ Returns table with classes statistics to be printed.
        TABLE OPTIONS can be: types, individuals, total.
        BORDER OPTIONS can be all values accepted by prettytable lib.
        """

    logger = initialize_logger()

    if list_values_classes[0] != list_values_classes[10]:
        logger.error("Number of classes must be the same before and after the software execution. Program aborted.")
        exit(1)

    # CALCULATIONS FOR CLASSES ----------------------------------------------------------------

    # COLUMN BEFORE - CLASSES BEFORE

    # Values

    classes_before = list_values_classes[0]

    tu_classes_types_b_v = list_values_classes[1]
    tu_classes_individuals_b_v = list_values_classes[2]
    tu_classes_total_b_v = list_values_classes[3]

    pk_classes_types_b_v = list_values_classes[4]
    pk_classes_individuals_b_v = list_values_classes[5]
    pk_classes_total_b_v = list_values_classes[6]

    tk_classes_types_b_v = list_values_classes[7]
    tk_classes_individuals_b_v = list_values_classes[8]
    tk_classes_total_b_v = list_values_classes[9]

    # Percentages

    tu_classes_types_b_p = (tu_classes_types_b_v / classes_before) * 100
    tu_classes_individuals_b_p = (tu_classes_individuals_b_v / classes_before) * 100
    tu_classes_total_b_p = (tu_classes_total_b_v / classes_before) * 100

    pk_classes_types_b_p = (pk_classes_types_b_v / classes_before) * 100
    pk_classes_individuals_b_p = (pk_classes_individuals_b_v / classes_before) * 100
    pk_classes_total_b_p = (pk_classes_total_b_v / classes_before) * 100

    tk_classes_types_b_p = (tk_classes_types_b_v / classes_before) * 100
    tk_classes_individuals_b_p = (tk_classes_individuals_b_v / classes_before) * 100
    tk_classes_total_b_p = (tk_classes_total_b_v / classes_before) * 100

    # COLUMN AFTER - CLASSES AFTER

    # Values

    classes_after = list_values_classes[10]

    tu_classes_types_a_v = list_values_classes[11]
    tu_classes_individuals_a_v = list_values_classes[12]
    tu_classes_total_a_v = list_values_classes[13]

    pk_classes_types_a_v = list_values_classes[14]
    pk_classes_individuals_a_v = list_values_classes[15]
    pk_classes_total_a_v = list_values_classes[16]

    tk_classes_types_a_v = list_values_classes[17]
    tk_classes_individuals_a_v = list_values_classes[18]
    tk_classes_total_a_v = list_values_classes[19]

    # Percentages

    tu_classes_types_a_p = (tu_classes_types_a_v / classes_after) * 100
    tu_classes_individuals_a_p = (tu_classes_individuals_a_v / classes_after) * 100
    tu_classes_total_a_p = (tu_classes_total_a_v / classes_after) * 100

    pk_classes_types_a_p = (pk_classes_types_a_v / classes_after) * 100
    pk_classes_individuals_a_p = (pk_classes_individuals_a_v / classes_after) * 100
    pk_classes_total_a_p = (pk_classes_total_a_v / classes_after) * 100

    tk_classes_types_a_p = (tk_classes_types_a_v / classes_after) * 100
    tk_classes_individuals_a_p = (tk_classes_individuals_a_v / classes_after) * 100
    tk_classes_total_a_p = (tk_classes_total_a_v / classes_after) * 100

    # COLUMN DIFFERENCE - CLASSES BEFORE x AFTER

    # Values

    tu_classes_types_ba_v = tu_classes_types_a_v - tu_classes_types_b_v
    tu_classes_individuals_ba_v = tu_classes_individuals_a_v - tu_classes_individuals_b_v
    tu_classes_total_ba_v = tu_classes_total_a_v - tu_classes_total_b_v

    pk_classes_types_ba_v = pk_classes_types_a_v - pk_classes_types_b_v
    pk_classes_individuals_ba_v = pk_classes_individuals_a_v - pk_classes_individuals_b_v
    pk_classes_total_ba_v = pk_classes_total_a_v - pk_classes_total_b_v

    tk_classes_types_ba_v = tk_classes_types_a_v - tk_classes_types_b_v
    tk_classes_individuals_ba_v = tk_classes_individuals_a_v - tk_classes_individuals_b_v
    tk_classes_total_ba_v = tk_classes_total_a_v - tk_classes_total_b_v

    # Percentages

    tu_classes_types_ba_p = tu_classes_types_a_p - tu_classes_types_b_p
    tu_classes_individuals_ba_p = tu_classes_individuals_a_p - tu_classes_individuals_b_p
    tu_classes_total_ba_p = tu_classes_total_a_p - tu_classes_total_b_p

    pk_classes_types_ba_p = pk_classes_types_a_p - pk_classes_types_b_p
    pk_classes_individuals_ba_p = pk_classes_individuals_a_p - pk_classes_individuals_b_p
    pk_classes_total_ba_p = pk_classes_total_a_p - pk_classes_total_b_p

    tk_classes_types_ba_p = tk_classes_types_a_p - tk_classes_types_b_p
    tk_classes_individuals_ba_p = tk_classes_individuals_a_p - tk_classes_individuals_b_p
    tk_classes_total_ba_p = tk_classes_total_a_p - tk_classes_total_b_p

    # TABLES GENERATION ----------------------------------------------------------------

    # Tables' columns' titles
    columns_titles = ["Evaluation", "Before", "After", "Difference     "]

    pretty_table = PrettyTable(columns_titles)

    # Tables' rows' titles
    row_1 = "Total number of classes"

    pos_r1_c1 = f"{classes_before} ({100.00}%)"
    pos_r1_c2 = f"{classes_after} ({100.00}%)"
    pos_r1_c3 = f"{classes_before - classes_after} ({0.00}%)"

    row_2 = "Totally unknown classes"
    row_3 = "Partially known classes"
    row_4 = "Totally known classes"

    pos_r2_c1 = "undefined - error if printed"
    pos_r2_c2 = "undefined - error if printed"
    pos_r2_c3 = "undefined - error if printed"
    pos_r3_c1 = "undefined - error if printed"
    pos_r3_c2 = "undefined - error if printed"
    pos_r3_c3 = "undefined - error if printed"
    pos_r4_c1 = "undefined - error if printed"
    pos_r4_c2 = "undefined - error if printed"
    pos_r4_c3 = "undefined - error if printed"

    if table_option == "types":
        pos_r2_c1 = f"{tu_classes_types_b_v} ({round(tu_classes_types_b_p, 2)}%)"
        pos_r2_c2 = f"{tu_classes_types_a_v} ({round(tu_classes_types_a_p, 2)}%)"
        pos_r2_c3 = f"{tu_classes_types_ba_v} ({round(tu_classes_types_ba_p, 2)}%)"
        pos_r3_c1 = f"{pk_classes_types_b_v} ({round(pk_classes_types_b_p, 2)}%)"
        pos_r3_c2 = f"{pk_classes_types_a_v} ({round(pk_classes_types_a_p, 2)}%)"
        pos_r3_c3 = f"{pk_classes_types_ba_v} ({round(pk_classes_types_ba_p, 2)}%)"
        pos_r4_c1 = f"{tk_classes_types_b_v} ({round(tk_classes_types_b_p, 2)}%)"
        pos_r4_c2 = f"{tk_classes_types_a_v} ({round(tk_classes_types_a_p, 2)}%)"
        pos_r4_c3 = f"{tk_classes_types_ba_v} ({round(tk_classes_types_ba_p, 2)}%)"
    elif table_option == "individuals":
        pos_r2_c1 = f"{tu_classes_individuals_b_v} ({round(tu_classes_individuals_b_p, 2)}%)"
        pos_r2_c2 = f"{tu_classes_individuals_a_v} ({round(tu_classes_individuals_a_p, 2)}%)"
        pos_r2_c3 = f"{tu_classes_individuals_ba_v} ({round(tu_classes_individuals_ba_p, 2)}%)"
        pos_r3_c1 = f"{pk_classes_individuals_b_v} ({round(pk_classes_individuals_b_p, 2)}%)"
        pos_r3_c2 = f"{pk_classes_individuals_a_v} ({round(pk_classes_individuals_a_p, 2)}%)"
        pos_r3_c3 = f"{pk_classes_individuals_ba_v} ({round(pk_classes_individuals_ba_p, 2)}%)"
        pos_r4_c1 = f"{tk_classes_individuals_b_v} ({round(tk_classes_individuals_b_p, 2)}%)"
        pos_r4_c2 = f"{tk_classes_individuals_a_v} ({round(tk_classes_individuals_a_p, 2)}%)"
        pos_r4_c3 = f"{tk_classes_individuals_ba_v} ({round(tk_classes_individuals_ba_p, 2)}%)"
    elif table_option == "total":
        pos_r2_c1 = f"{tu_classes_total_b_v} ({round(tu_classes_total_b_p, 2)}%)"
        pos_r2_c2 = f"{tu_classes_total_a_v} ({round(tu_classes_total_a_p, 2)}%)"
        pos_r2_c3 = f"{tu_classes_total_ba_v} ({round(tu_classes_total_ba_p, 2)}%)"
        pos_r3_c1 = f"{pk_classes_total_b_v} ({round(pk_classes_total_b_p, 2)}%)"
        pos_r3_c2 = f"{pk_classes_total_a_v} ({round(pk_classes_total_a_p, 2)}%)"
        pos_r3_c3 = f"{pk_classes_total_ba_v} ({round(pk_classes_total_ba_p, 2)}%)"
        pos_r4_c1 = f"{tk_classes_total_b_v} ({round(tk_classes_total_b_p, 2)}%)"
        pos_r4_c2 = f"{tk_classes_total_a_v} ({round(tk_classes_total_a_p, 2)}%)"
        pos_r4_c3 = f"{tk_classes_total_ba_v} ({round(tk_classes_total_ba_p, 2)}%)"
    else:
        logger.error("Invalid table option. Program aborted.")
        exit(1)

    pretty_table.add_row([row_1, pos_r1_c1, pos_r1_c2, pos_r1_c3])
    pretty_table.add_row([row_2, pos_r2_c1, pos_r2_c2, pos_r2_c3])
    pretty_table.add_row([row_3, pos_r3_c1, pos_r3_c2, pos_r3_c3])
    pretty_table.add_row([row_4, pos_r4_c1, pos_r4_c2, pos_r4_c3])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    return pretty_table


def print_statistics_screen(list_values_classes, list_values_classifications, restriction="PRINT_ALL"):
    """ Receives lists of before and after values and prints them in a table.

    Restrictions:
        - "PRINT_ALL" - prints total, individuals, and total tables.
        - "total_ONLY" - prints only total table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    list_values positions:

        FOR NUMBERS OF CLASSES:
            return_list_classes[0] = total_classes_number

            return_list_classes[1] = totally_unknown_classes_total
            return_list_classes[2] = totally_unknown_classes_individuals
            return_list_classes[3] = totally_unknown_classes_all

            return_list_classes[4] = partially_known_classes_total
            return_list_classes[5] = partially_known_classes_individuals
            return_list_classes[6] = partially_known_classes_all

            return_list_classes[7] = totally_known_classes_total
            return_list_classes[8] = totally_known_classes_individuals
            return_list_classes[9] = totally_known_classes_all

        FOR NUMBERS OF CLASSIFICATIONS:
            return_list_classifications[0] = total_classifications_number

            return_list_classifications[1] = total_classifications_total
            return_list_classifications[2] = total_classifications_individuals

            return_list_classifications[3] = number_unknown_classifications_total
            return_list_classifications[4] = number_known_classifications_total

            return_list_classifications[5] = number_unknown_classifications_individuals
            return_list_classifications[6] = number_known_classifications_individuals

            return_list_classifications[7] = number_unknown_classifications_total
            return_list_classifications[8] = number_known_classifications_total
    """

    logger = initialize_logger()

    print("\n##### FINAL ONTCATOWL CLASSIFICATION SUMMARY #####")

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        table_classes_types = generate_classes_table_to_be_printed(list_values_classes, "types", SINGLE_BORDER)
        # table_classifications_types = generate_classifications_table_to_be_printed(list_values_classifications, "types", SINGLE_BORDER)

        print(f"\nResults of OntCatOWL execution when evaluating TYPES:")

        print(table_classes_types)

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        table_classes_individuals = generate_classes_table_to_be_printed(list_values_classes, "individuals",
                                                                         SINGLE_BORDER)

        print(f"\nResults of OntCatOWL execution when evaluating INDIVIDUALS:")

        print(table_classes_individuals)

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        table_classes_total = generate_classes_table_to_be_printed(list_values_classes, "total", SINGLE_BORDER)

        print(
            f"\nResults of OntCatOWL execution when evaluating TYPES and INDIVIDUALS:")

        print(table_classes_total)
