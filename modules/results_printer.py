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
    columns_titles = ["Evaluation", "        Before", "         After", "    Difference"]

    pretty_table = PrettyTable(columns_titles)

    # Tables' rows' titles

    row_1 = "Totally unknown classes"
    row_2 = "Partially known classes"
    row_3 = "Totally known classes"

    pos_r1_c1 = "undefined - error if printed"
    pos_r1_c2 = "undefined - error if printed"
    pos_r1_c3 = "undefined - error if printed"
    pos_r2_c1 = "undefined - error if printed"
    pos_r2_c2 = "undefined - error if printed"
    pos_r2_c3 = "undefined - error if printed"
    pos_r3_c1 = "undefined - error if printed"
    pos_r3_c2 = "undefined - error if printed"
    pos_r3_c3 = "undefined - error if printed"

    if table_option == "types":

        message = f"\nResults of OntCatOWL execution when evaluating {classes_before} CLASSES " \
                  f"considering only TYPES:\n"

        pos_r1_c1 = f"{tu_classes_types_b_v} ({round(tu_classes_types_b_p, 2)}%)"
        pos_r1_c2 = f"{tu_classes_types_a_v} ({round(tu_classes_types_a_p, 2)}%)"
        pos_r1_c3 = f"{tu_classes_types_ba_v} ({round(tu_classes_types_ba_p, 2)}%)"
        pos_r2_c1 = f"{pk_classes_types_b_v} ({round(pk_classes_types_b_p, 2)}%)"
        pos_r2_c2 = f"{pk_classes_types_a_v} ({round(pk_classes_types_a_p, 2)}%)"
        pos_r2_c3 = f"{pk_classes_types_ba_v} ({round(pk_classes_types_ba_p, 2)}%)"
        pos_r3_c1 = f"{tk_classes_types_b_v} ({round(tk_classes_types_b_p, 2)}%)"
        pos_r3_c2 = f"{tk_classes_types_a_v} ({round(tk_classes_types_a_p, 2)}%)"
        pos_r3_c3 = f"{tk_classes_types_ba_v} ({round(tk_classes_types_ba_p, 2)}%)"
    elif table_option == "individuals":

        message = f"\nResults of OntCatOWL execution when evaluating {classes_before} CLASSES " \
                  f"considering only INDIVIDUALS:\n"

        pos_r1_c1 = f"{tu_classes_individuals_b_v} ({round(tu_classes_individuals_b_p, 2)}%)"
        pos_r1_c2 = f"{tu_classes_individuals_a_v} ({round(tu_classes_individuals_a_p, 2)}%)"
        pos_r1_c3 = f"{tu_classes_individuals_ba_v} ({round(tu_classes_individuals_ba_p, 2)}%)"
        pos_r2_c1 = f"{pk_classes_individuals_b_v} ({round(pk_classes_individuals_b_p, 2)}%)"
        pos_r2_c2 = f"{pk_classes_individuals_a_v} ({round(pk_classes_individuals_a_p, 2)}%)"
        pos_r2_c3 = f"{pk_classes_individuals_ba_v} ({round(pk_classes_individuals_ba_p, 2)}%)"
        pos_r3_c1 = f"{tk_classes_individuals_b_v} ({round(tk_classes_individuals_b_p, 2)}%)"
        pos_r3_c2 = f"{tk_classes_individuals_a_v} ({round(tk_classes_individuals_a_p, 2)}%)"
        pos_r3_c3 = f"{tk_classes_individuals_ba_v} ({round(tk_classes_individuals_ba_p, 2)}%)"
    elif table_option == "total":

        message = f"\nResults of OntCatOWL execution when evaluating {classes_before} CLASSES " \
                  f"considering TYPES and  INDIVIDUALS:\n"

        pos_r1_c1 = f"{tu_classes_total_b_v} ({round(tu_classes_total_b_p, 2)}%)"
        pos_r1_c2 = f"{tu_classes_total_a_v} ({round(tu_classes_total_a_p, 2)}%)"
        pos_r1_c3 = f"{tu_classes_total_ba_v} ({round(tu_classes_total_ba_p, 2)}%)"
        pos_r2_c1 = f"{pk_classes_total_b_v} ({round(pk_classes_total_b_p, 2)}%)"
        pos_r2_c2 = f"{pk_classes_total_a_v} ({round(pk_classes_total_a_p, 2)}%)"
        pos_r2_c3 = f"{pk_classes_total_ba_v} ({round(pk_classes_total_ba_p, 2)}%)"
        pos_r3_c1 = f"{tk_classes_total_b_v} ({round(tk_classes_total_b_p, 2)}%)"
        pos_r3_c2 = f"{tk_classes_total_a_v} ({round(tk_classes_total_a_p, 2)}%)"
        pos_r3_c3 = f"{tk_classes_total_ba_v} ({round(tk_classes_total_ba_p, 2)}%)"
    else:
        logger.error("Invalid table option. Program aborted.")
        exit(1)

    pretty_table.add_row([row_1, pos_r1_c1, pos_r1_c2, pos_r1_c3])
    pretty_table.add_row([row_2, pos_r2_c1, pos_r2_c2, pos_r2_c3])
    pretty_table.add_row([row_3, pos_r3_c1, pos_r3_c2, pos_r3_c3])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def generate_classifications_table_to_be_printed(list_values_classifications, table_option, border_option):
    """ Returns table with classifications statistics to be printed.
        TABLE OPTIONS can be: types, individuals, total.
        BORDER OPTIONS can be all values accepted by prettytable lib.
        """

    logger = initialize_logger()

    if list_values_classifications[0] != list_values_classifications[10]:
        logger.error("Number of classifications must be the same before and after the software execution. "
                     "Program aborted.")
        exit(1)

    # CALCULATIONS FOR classifications ----------------------------------------------------------------

    # COLUMN BEFORE - classifications BEFORE

    # Values

    total_number_classif_b_v = list_values_classifications[0]

    total_classif_types_b_v = list_values_classifications[1]
    total_classif_individuals_b_v = list_values_classifications[2]

    number_unknown_classif_types_b_v = list_values_classifications[3]
    number_known_classif_types_b_v = list_values_classifications[4]

    number_unknown_classif_individuals_b_v = list_values_classifications[5]
    number_known_classif_individuals_b_v = list_values_classifications[6]

    number_unknown_classif_total_b_v = list_values_classifications[7]
    number_known_classif_total_b_v = list_values_classifications[8]

    # Percentages

    number_unknown_classif_types_b_p = (number_unknown_classif_types_b_v / total_classif_types_b_v) * 100
    number_known_classif_types_b_p = (number_known_classif_types_b_v / total_classif_types_b_v) * 100

    number_unknown_classif_individuals_b_p = (number_unknown_classif_individuals_b_v /
                                              total_classif_individuals_b_v) * 100
    number_known_classif_individuals_b_p = (number_known_classif_individuals_b_v / total_classif_individuals_b_v) * 100

    number_unknown_classif_total_b_p = (number_unknown_classif_total_b_v / total_number_classif_b_v) * 100
    number_known_classif_total_b_p = (number_known_classif_total_b_v / total_number_classif_b_v) * 100

    # COLUMN AFTER - classifications AFTER

    # Values

    total_number_classif_a_v = list_values_classifications[10]

    total_classif_types_a_v = list_values_classifications[11]
    total_classif_individuals_a_v = list_values_classifications[12]

    number_unknown_classif_types_a_v = list_values_classifications[13]
    number_known_classif_types_a_v = list_values_classifications[14]

    number_unknown_classif_individuals_a_v = list_values_classifications[15]
    number_known_classif_individuals_a_v = list_values_classifications[16]

    number_unknown_classif_total_a_v = list_values_classifications[17]
    number_known_classif_total_a_v = list_values_classifications[18]

    # Percentages

    number_unknown_classif_types_a_p = (number_unknown_classif_types_a_v / total_classif_types_a_v) * 100
    number_known_classif_types_a_p = (number_known_classif_types_a_v / total_classif_types_a_v) * 100

    number_unknown_classif_individuals_a_p = (number_unknown_classif_individuals_a_v /
                                              total_classif_individuals_a_v) * 100
    number_known_classif_individuals_a_p = (number_known_classif_individuals_a_v / total_classif_individuals_a_v) * 100

    number_unknown_classif_total_a_p = (number_unknown_classif_total_a_v / total_number_classif_a_v) * 100
    number_known_classif_total_a_p = (number_known_classif_total_a_v / total_number_classif_a_v) * 100

    # COLUMN DIFFERENCE - classifications BEFORE x AFTER

    # Values

    number_unknown_classif_types_ba_v = number_unknown_classif_types_a_v - number_unknown_classif_types_b_v
    number_known_classif_types_ba_v = number_known_classif_types_a_v - number_known_classif_types_b_v

    number_unknown_classif_individuals_ba_v = number_unknown_classif_individuals_a_v - \
                                              number_unknown_classif_individuals_b_v
    number_known_classif_individuals_ba_v = number_known_classif_individuals_a_v - number_known_classif_individuals_b_v

    number_unknown_classif_total_ba_v = number_unknown_classif_total_a_v - number_unknown_classif_total_b_v
    number_known_classif_total_ba_v = number_known_classif_total_a_v - number_known_classif_total_b_v

    # Percentages

    number_unknown_classif_types_ba_p = number_unknown_classif_types_a_p - number_unknown_classif_types_b_p
    number_known_classif_types_ba_p = number_known_classif_types_a_p - number_known_classif_types_b_p

    number_unknown_classif_individuals_ba_p = number_unknown_classif_individuals_a_p - \
                                              number_unknown_classif_individuals_b_p
    number_known_classif_individuals_ba_p = number_known_classif_individuals_a_p - number_known_classif_individuals_b_p

    number_unknown_classif_total_ba_p = number_unknown_classif_total_a_p - number_unknown_classif_total_b_p
    number_known_classif_total_ba_p = number_known_classif_total_a_p - number_known_classif_total_b_p

    # TABLES GENERATION ----------------------------------------------------------------

    # Tables' columns' titles
    columns_titles = ["Evaluation", "        Before", "         After", "    Difference"]

    pretty_table = PrettyTable(columns_titles)

    # Tables' rows' titles

    row_1 = "Unknown classifications"
    row_2 = "Known classifications"

    pos_r1_c1 = "undefined - error if printed"
    pos_r1_c2 = "undefined - error if printed"
    pos_r1_c3 = "undefined - error if printed"
    pos_r2_c1 = "undefined - error if printed"
    pos_r2_c2 = "undefined - error if printed"
    pos_r2_c3 = "undefined - error if printed"

    message = ""
    if table_option == "types":

        message = f"\nResults of OntCatOWL execution when evaluating {total_classif_types_a_v} " \
                  f"CLASSIFICATIONS considering only TYPES:\n"

        pos_r1_c1 = f"{number_unknown_classif_types_b_v} ({round(number_unknown_classif_types_b_p, 2)}%)"
        pos_r1_c2 = f"{number_unknown_classif_types_a_v} ({round(number_unknown_classif_types_a_p, 2)}%)"
        pos_r1_c3 = f"{number_unknown_classif_types_ba_v} ({round(number_unknown_classif_types_ba_p, 2)}%)"
        pos_r2_c1 = f"{number_known_classif_types_b_v} ({round(number_known_classif_types_b_p, 2)}%)"
        pos_r2_c2 = f"{number_known_classif_types_a_v} ({round(number_known_classif_types_a_p, 2)}%)"
        pos_r2_c3 = f"{number_known_classif_types_ba_v} ({round(number_known_classif_types_ba_p, 2)}%)"
    elif table_option == "individuals":

        message = f"\nResults of OntCatOWL execution when evaluating {total_classif_individuals_a_v} " \
                  f"CLASSIFICATIONS considering only INDIVIDUALS:\n"

        pos_r1_c1 = f"{number_unknown_classif_individuals_b_v} ({round(number_unknown_classif_individuals_b_p, 2)}%)"
        pos_r1_c2 = f"{number_unknown_classif_individuals_a_v} ({round(number_unknown_classif_individuals_a_p, 2)}%)"
        pos_r1_c3 = f"{number_unknown_classif_individuals_ba_v} ({round(number_unknown_classif_individuals_ba_p, 2)}%)"
        pos_r2_c1 = f"{number_known_classif_individuals_b_v} ({round(number_known_classif_individuals_b_p, 2)}%)"
        pos_r2_c2 = f"{number_known_classif_individuals_a_v} ({round(number_known_classif_individuals_a_p, 2)}%)"
        pos_r2_c3 = f"{number_known_classif_individuals_ba_v} ({round(number_known_classif_individuals_ba_p, 2)}%)"
    elif table_option == "total":

        message = f"\nResults of OntCatOWL execution when evaluating {total_number_classif_a_v} " \
                  f"CLASSIFICATIONS considering TYPES and INDIVIDUALS:\n"

        pos_r1_c1 = f"{number_unknown_classif_total_b_v} ({round(number_unknown_classif_total_b_p, 2)}%)"
        pos_r1_c2 = f"{number_unknown_classif_total_a_v} ({round(number_unknown_classif_total_a_p, 2)}%)"
        pos_r1_c3 = f"{number_unknown_classif_total_ba_v} ({round(number_unknown_classif_total_ba_p, 2)}%)"
        pos_r2_c1 = f"{number_known_classif_total_b_v} ({round(number_known_classif_total_b_p, 2)}%)"
        pos_r2_c2 = f"{number_known_classif_total_a_v} ({round(number_known_classif_total_a_p, 2)}%)"
        pos_r2_c3 = f"{number_known_classif_total_ba_v} ({round(number_known_classif_total_ba_p, 2)}%)"
    else:
        logger.error("Invalid table option. Program aborted.")
        exit(1)

    pretty_table.add_row([row_1, pos_r1_c1, pos_r1_c2, pos_r1_c3])
    pretty_table.add_row([row_2, pos_r2_c1, pos_r2_c2, pos_r2_c3])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def print_statistics_screen(list_values_classes, list_values_classifications, restriction="PRINT_ALL"):
    """ Receives lists of before and after values and prints them in a table.

    Restrictions:
        - "PRINT_ALL" - prints total, individuals, and total tables.
        - "TYPES_ONLY" - prints only total table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    list_values positions:

        FOR NUMBERS OF CLASSES:
            list_values_classes[(1)0] = total_classes_number

            list_values_classes[(1)1] = totally_unknown_classes_total
            list_values_classes[(1)2] = totally_unknown_classes_individuals
            list_values_classes[(1)3] = totally_unknown_classes_all

            list_values_classes[(1)4] = partially_known_classes_total
            list_values_classes[(1)5] = partially_known_classes_individuals
            list_values_classes[(1)6] = partially_known_classes_all

            list_values_classes[(1)7] = totally_known_classes_total
            list_values_classes[(1)8] = totally_known_classes_individuals
            list_values_classes[(1)9] = totally_known_classes_all

        FOR NUMBERS OF CLASSIFICATIONS:
            list_values_classifications[(1)0] = total_classifications_number

            list_values_classifications[(1)1] = total_classifications_types
            list_values_classifications[(1)2] = total_classifications_individuals

            list_values_classifications[(1)3] = number_unknown_classifications_types
            list_values_classifications[(1)4] = number_known_classifications_types

            list_values_classifications[(1)5] = number_unknown_classifications_individuals
            list_values_classifications[(1)6] = number_known_classifications_individuals

            list_values_classifications[(1)7] = number_unknown_classifications_total
            list_values_classifications[(1)8] = number_known_classifications_total

            list_values_classifications[(1)0] = 0 (empty)
    """

    print("\n##### FINAL ONTCATOWL CLASSIFICATION SUMMARY #####")

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        table_classes_types = generate_classes_table_to_be_printed(list_values_classes, "types", SINGLE_BORDER)
        table_classifications_types = generate_classifications_table_to_be_printed(list_values_classifications, "types",
                                                                                   SINGLE_BORDER)

        print(table_classes_types)
        print(table_classifications_types)
        print()

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        table_classes_individuals = generate_classes_table_to_be_printed(list_values_classes, "individuals",
                                                                         SINGLE_BORDER)
        table_classifications_individuals = generate_classifications_table_to_be_printed(list_values_classifications,
                                                                                         "individuals", SINGLE_BORDER)

        print(table_classes_individuals)
        print(table_classifications_individuals)
        print()

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        table_classes_total = generate_classes_table_to_be_printed(list_values_classes, "total", SINGLE_BORDER)
        table_classifications_total = generate_classifications_table_to_be_printed(list_values_classifications, "total",
                                                                                   SINGLE_BORDER)

        print(table_classes_total)
        print(table_classifications_total)
        print()
