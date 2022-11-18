""" Fucntions for printing statistics to the user. """
from prettytable import PrettyTable, SINGLE_BORDER

from modules.logger_config import initialize_logger


def generate_times_table_to_be_printed(time_register, border_option):
    """ Generates table with aggregated execution times for all rules to be printed. """

    total_rules_time = round(
        time_register["k_s_sup"] + time_register["s_k_sub"] + time_register["t_k_sup"] + time_register["ns_s_sup"] +
        time_register["s_ns_sub"] + time_register["r_ar_sup"] + time_register["ar_r_sub"] + time_register["ns_sub_r"] +
        time_register["ks_sf_in"] + time_register["n_r_t"] + time_register["ns_s_spe"] + time_register["nk_k_sup"] +
        time_register["s_nsup_k"] + time_register["nrs_ns_r"], 3)

    # Tables' columns' titles
    columns_titles = ["Rule Code", " Time (s)"]

    pretty_table = PrettyTable(columns_titles)

    message = f"\nTotal aggregated execution times for all rules was {total_rules_time} seconds:\n"

    pretty_table.add_row(["ar_r_sub", round(time_register["ar_r_sub"], 3)])
    pretty_table.add_row(["k_s_sup", round(time_register["k_s_sup"], 3)])
    pretty_table.add_row(["ks_sf_in", round(time_register["ks_sf_in"], 3)])
    pretty_table.add_row(["n_r_t", round(time_register["n_r_t"], 3)])
    pretty_table.add_row(["nk_k_sup", round(time_register["nk_k_sup"], 3)])
    pretty_table.add_row(["nrs_ns_r", round(time_register["nrs_ns_r"], 3)])
    pretty_table.add_row(["ns_s_spe", round(time_register["ns_s_spe"], 3)])
    pretty_table.add_row(["ns_s_sup", round(time_register["ns_s_sup"], 3)])
    pretty_table.add_row(["ns_sub_r", round(time_register["ns_sub_r"], 3)])
    pretty_table.add_row(["r_ar_sup", round(time_register["r_ar_sup"], 3)])
    pretty_table.add_row(["s_k_sub", round(time_register["s_k_sub"], 3)])
    pretty_table.add_row(["s_ns_sub", round(time_register["s_ns_sub"], 3)])
    pretty_table.add_row(["s_nsup_k", round(time_register["s_nsup_k"], 3)])
    pretty_table.add_row(["t_k_sup", round(time_register["t_k_sup"], 3)])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def generate_classes_table_to_be_printed(before_after_statistics, table_option, border_option):
    """ Returns table with classes statistics to be printed.
        TABLE OPTIONS can be: types, individuals, total.
        BORDER OPTIONS can be all values accepted by prettytable lib.
    """

    logger = initialize_logger()

    # CALCULATIONS FOR CLASSES ----------------------------------------------------------------

    # COLUMN BEFORE - CLASSES BEFORE

    # Values

    before = before_after_statistics.classes_statistics_before
    after = before_after_statistics.classes_statistics_after

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

        pos_r1_c1 = f"{before.totally_unknown_classes_types} ({round(tu_classes_types_b_p, 2)}%)"
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

        pos_r1_c1 = f"{before.totally_unknown_classes_individuals} ({round(tu_classes_individuals_b_p, 2)}%)"
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

        pos_r1_c1 = f"{before.totally_unknown_classes_all} ({round(tu_classes_total_b_p, 2)}%)"
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


def print_statistics_screen(before_after_statistics, time_register, configurations,
                            restriction="PRINT_ALL"):
    """ Receives list of execution times, and lists of before and after values and prints these three statistics.

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
        table_classes_types = generate_classes_table_to_be_printed(before_after_statistics, "types", SINGLE_BORDER)
        table_classifications_types = generate_classifications_table_to_be_printed(before_after_statistics, "types",
                                                                                   SINGLE_BORDER)

        print(table_classes_types)
        print(table_classifications_types)

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        table_classes_individuals = generate_classes_table_to_be_printed(before_after_statistics, "individuals",
                                                                         SINGLE_BORDER)
        table_classifications_individuals = generate_classifications_table_to_be_printed(before_after_statistics,
                                                                                         "individuals", SINGLE_BORDER)

        print(table_classes_individuals)
        print(table_classifications_individuals)

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        table_classes_total = generate_classes_table_to_be_printed(before_after_statistics, "total", SINGLE_BORDER)
        table_classifications_total = generate_classifications_table_to_be_printed(before_after_statistics, "total",
                                                                                   SINGLE_BORDER)

        print(table_classes_total)
        print(table_classifications_total)

    if configurations["print_time"]:
        table_aggregated_time = generate_times_table_to_be_printed(time_register, SINGLE_BORDER)
        print(table_aggregated_time)

    print()
