""" Fucntions for printing statistics to the user. """
import operator

from prettytable import PrettyTable, SINGLE_BORDER

from ontcatowl.modules.logger_config import initialize_logger


def generate_times_table(time_register, border_option):
    """ Generates table with aggregated execution times for all rules to be printed. """

    total_rules_time = round(time_register["total_time"], 3)

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


def generate_classes_table(consolidated_statistics, table_option, border_option):
    """ Returns table with classes statistics to be printed.
        TABLE OPTIONS can be: types, individuals, total.
        BORDER OPTIONS can be all values accepted by prettytable lib.
    """

    logger = initialize_logger()

    before = consolidated_statistics.classes_stats_b
    after = consolidated_statistics.classes_stats_a
    ba = consolidated_statistics

    # TABLES GENERATION ----------------------------------------------------------------

    # Tables' columns' titles
    columns_titles = ["Evaluation", "        Before", "         After", "    Difference"]

    pretty_table = PrettyTable(columns_titles)

    # Tables' rows' titles

    row_1 = "Totally unknown classes"
    row_2 = "Partially known classes"
    row_3 = "Totally known classes"

    pos_r1_c1 = "undefined - error if printed."
    pos_r1_c2 = "undefined - error if printed."
    pos_r1_c3 = "undefined - error if printed."
    pos_r2_c1 = "undefined - error if printed."
    pos_r2_c2 = "undefined - error if printed."
    pos_r2_c3 = "undefined - error if printed."
    pos_r3_c1 = "undefined - error if printed."
    pos_r3_c2 = "undefined - error if printed."
    pos_r3_c3 = "undefined - error if printed."
    message = "undefined - error if printed."

    if table_option == "types":

        message = f"\nResults of OntCatOWL execution when evaluating {after.total_classes_number} CLASSES " \
                  f"considering only TYPES:\n"

        pos_r1_c1 = f"{before.tu_classes_types_v} ({round(before.tu_classes_types_p, 2)}%)"
        pos_r1_c2 = f"{after.tu_classes_types_v} ({round(after.tu_classes_types_p, 2)}%)"
        pos_r1_c3 = f"{ba.tu_classes_types_v_d} ({round(ba.tu_classes_types_p_d, 2)}%)"
        pos_r2_c1 = f"{before.pk_classes_types_v} ({round(before.pk_classes_types_p, 2)}%)"
        pos_r2_c2 = f"{after.pk_classes_types_v} ({round(after.pk_classes_types_p, 2)}%)"
        pos_r2_c3 = f"{ba.pk_classes_types_v_d} ({round(ba.pk_classes_types_p_d, 2)}%)"
        pos_r3_c1 = f"{before.tk_classes_types_v} ({round(before.tk_classes_types_p, 2)}%)"
        pos_r3_c2 = f"{after.tk_classes_types_v} ({round(after.tk_classes_types_p, 2)}%)"
        pos_r3_c3 = f"{ba.tk_classes_types_v_d} ({round(ba.tk_classes_types_p_d, 2)}%)"

    elif table_option == "individuals":

        message = f"\nResults of OntCatOWL execution when evaluating {after.total_classes_number} CLASSES " \
                  f"considering only INDIVIDUALS:\n"

        pos_r1_c1 = f"{before.tu_classes_indiv_v} ({round(before.tu_classes_indiv_p, 2)}%)"
        pos_r1_c2 = f"{after.tu_classes_indiv_v} ({round(after.tu_classes_indiv_p, 2)}%)"
        pos_r1_c3 = f"{ba.tu_classes_indiv_v_d} ({round(ba.tu_classes_indiv_p_d, 2)}%)"
        pos_r2_c1 = f"{before.pk_classes_indiv_v} ({round(before.pk_classes_indiv_p, 2)}%)"
        pos_r2_c2 = f"{after.pk_classes_indiv_v} ({round(after.pk_classes_indiv_p, 2)}%)"
        pos_r2_c3 = f"{ba.pk_classes_indiv_v_d} ({round(ba.pk_classes_indiv_p_d, 2)}%)"
        pos_r3_c1 = f"{before.tk_classes_indiv_v} ({round(before.tk_classes_indiv_p, 2)}%)"
        pos_r3_c2 = f"{after.tk_classes_indiv_v} ({round(after.tk_classes_indiv_p, 2)}%)"
        pos_r3_c3 = f"{ba.tk_classes_indiv_v_d} ({round(ba.tk_classes_indiv_p_d, 2)}%)"

    elif table_option == "total":

        message = f"\nResults of OntCatOWL execution when evaluating {after.total_classes_number} CLASSES " \
                  f"considering TYPES and  INDIVIDUALS:\n"

        pos_r1_c1 = f"{before.tu_classes_all_v} ({round(before.tu_classes_all_p, 2)}%)"
        pos_r1_c2 = f"{after.tu_classes_all_v} ({round(after.tu_classes_all_p, 2)}%)"
        pos_r1_c3 = f"{ba.tu_classes_all_v_d} ({round(ba.tu_classes_all_p_d, 2)}%)"
        pos_r2_c1 = f"{before.pk_classes_all_v} ({round(before.pk_classes_all_p, 2)}%)"
        pos_r2_c2 = f"{after.pk_classes_all_v} ({round(after.pk_classes_all_p, 2)}%)"
        pos_r2_c3 = f"{ba.pk_classes_all_v_d} ({round(ba.pk_classes_all_p_d, 2)}%)"
        pos_r3_c1 = f"{before.tk_classes_all_v} ({round(before.tk_classes_all_p, 2)}%)"
        pos_r3_c2 = f"{after.tk_classes_all_v} ({round(after.tk_classes_all_p, 2)}%)"
        pos_r3_c3 = f"{ba.tk_classes_all_v_d} ({round(ba.tk_classes_all_p_d, 2)}%)"
    else:
        logger.error(f"Invalid table option ({table_option}). Program aborted.")
        exit(1)

    pretty_table.add_row([row_1, pos_r1_c1, pos_r1_c2, pos_r1_c3])
    pretty_table.add_row([row_2, pos_r2_c1, pos_r2_c2, pos_r2_c3])
    pretty_table.add_row([row_3, pos_r3_c1, pos_r3_c2, pos_r3_c3])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def generate_classifications_table(consolidated_statistics, table_option, border_option):
    """ Returns table with classifications statistics to be printed.
        TABLE OPTIONS can be: types, individuals, total.
        BORDER OPTIONS can be all values accepted by prettytable lib.
        """

    logger = initialize_logger()

    before = consolidated_statistics.classif_stats_b
    after = consolidated_statistics.classif_stats_a
    ba = consolidated_statistics

    # Tables' columns' titles
    columns_titles = ["Evaluation", "        Before", "         After", "    Difference"]

    pretty_table = PrettyTable(columns_titles)

    # Tables' rows' titles

    row_1 = "Unknown classifications"
    row_2 = "Known classifications"

    pos_r1_c1 = "undefined - error if printed."
    pos_r1_c2 = "undefined - error if printed."
    pos_r1_c3 = "undefined - error if printed."
    pos_r2_c1 = "undefined - error if printed."
    pos_r2_c2 = "undefined - error if printed."
    pos_r2_c3 = "undefined - error if printed."
    message = "undefined - error if printed."

    if table_option == "types":

        message = f"\nResults of OntCatOWL execution when evaluating {before.total_classif_types_v} " \
                  f"CLASSIFICATIONS considering only TYPES:\n"

        pos_r1_c1 = f"{before.unknown_classif_types_v} ({round(before.unknown_classif_types_p, 2)}%)"
        pos_r1_c2 = f"{after.unknown_classif_types_v} ({round(after.unknown_classif_types_p, 2)}%)"
        pos_r1_c3 = f"{ba.unknown_classif_types_v_d} ({round(ba.unknown_classif_types_p_d, 2)}%)"
        pos_r2_c1 = f"{before.known_classif_types_v} ({round(before.known_classif_types_p, 2)}%)"
        pos_r2_c2 = f"{after.known_classif_types_v} ({round(after.known_classif_types_p, 2)}%)"
        pos_r2_c3 = f"{ba.known_classif_types_v_d} ({round(ba.known_classif_types_p_d, 2)}%)"

    elif table_option == "individuals":

        message = f"\nResults of OntCatOWL execution when evaluating {before.total_classif_indiv_v} " \
                  f"CLASSIFICATIONS considering only INDIVIDUALS:\n"

        pos_r1_c1 = f"{before.unknown_classif_indiv_v} ({round(before.unknown_classif_indiv_p, 2)}%)"
        pos_r1_c2 = f"{after.unknown_classif_indiv_v} ({round(after.unknown_classif_indiv_p, 2)}%)"
        pos_r1_c3 = f"{ba.unknown_classif_indiv_v_d} ({round(ba.unknown_classif_indiv_p_d, 2)}%)"
        pos_r2_c1 = f"{before.known_classif_indiv_v} ({round(before.known_classif_indiv_p, 2)}%)"
        pos_r2_c2 = f"{after.known_classif_indiv_v} ({round(after.known_classif_indiv_p, 2)}%)"
        pos_r2_c3 = f"{ba.known_classif_indiv_v_d} ({round(ba.known_classif_indiv_p_d, 2)}%)"
    elif table_option == "total":

        message = f"\nResults of OntCatOWL execution when evaluating {before.total_classif_number} " \
                  f"CLASSIFICATIONS considering TYPES and INDIVIDUALS:\n"

        pos_r1_c1 = f"{before.unknown_classif_total_v} ({round(before.unknown_classif_total_p, 2)}%)"
        pos_r1_c2 = f"{after.unknown_classif_total_v} ({round(after.unknown_classif_total_p, 2)}%)"
        pos_r1_c3 = f"{ba.unknown_classif_total_v_d} ({round(ba.unknown_classif_total_p_d, 2)}%)"
        pos_r2_c1 = f"{before.known_classif_total_v} ({round(before.known_classif_total_p, 2)}%)"
        pos_r2_c2 = f"{after.known_classif_total_v} ({round(after.known_classif_total_p, 2)}%)"
        pos_r2_c3 = f"{ba.known_classif_total_v_d} ({round(ba.known_classif_total_p_d, 2)}%)"
    else:
        logger.error(f"Invalid table option ({table_option}). Program aborted.")
        exit(1)

    pretty_table.add_row([row_1, pos_r1_c1, pos_r1_c2, pos_r1_c3])
    pretty_table.add_row([row_2, pos_r2_c1, pos_r2_c2, pos_r2_c3])

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def generate_incompleteness_table(ontology_dataclass_list, border_option):
    """ Generates a table with information about incomplete classes identified. """

    # Tables' columns' titles
    columns_titles = ["Incomplete Class", "Detection Rules"]

    pretty_table = PrettyTable(columns_titles)

    number_incomplete_classes = 0
    ontology_dataclass_list.sort(key=operator.attrgetter('uri'))

    for dataclass in ontology_dataclass_list:
        if dataclass.incompleteness_info["is_incomplete"] == True:
            pretty_table.add_row([dataclass.uri, dataclass.incompleteness_info["detected_in"]])
            number_incomplete_classes += 1

    message = f"\nA total of {number_incomplete_classes} classes were identified as incomplete.\n"

    pretty_table.align = "r"
    pretty_table.set_style(border_option)

    table_text = pretty_table.get_string()
    return_string = message + table_text

    return return_string


def print_statistics_screen(ontology_dataclass_list, consolidated_statistics, time_register, configurations,
                            restriction="PRINT_ALL"):
    """ Receives list of execution times, and lists of before and after values and prints these three statistics.

    Restrictions:
        - "PRINT_ALL" - prints total, individuals, and total tables.
        - "TYPES_ONLY" - prints only total table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    print("\n##### FINAL ONTCATOWL CLASSIFICATION SUMMARY #####")

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        table_classes_types = generate_classes_table(consolidated_statistics, "types", SINGLE_BORDER)
        table_classifications_types = generate_classifications_table(consolidated_statistics, "types",
                                                                     SINGLE_BORDER)

        print(table_classes_types)
        print(table_classifications_types)

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        table_classes_individuals = generate_classes_table(consolidated_statistics, "individuals",
                                                           SINGLE_BORDER)
        table_classifications_individuals = generate_classifications_table(consolidated_statistics,
                                                                           "individuals", SINGLE_BORDER)

        print(table_classes_individuals)
        print(table_classifications_individuals)

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        table_classes_total = generate_classes_table(consolidated_statistics, "total", SINGLE_BORDER)
        table_classifications_total = generate_classifications_table(consolidated_statistics, "total",
                                                                     SINGLE_BORDER)

        print(table_classes_total)
        print(table_classifications_total)

    table_incompleteness = generate_incompleteness_table(ontology_dataclass_list, SINGLE_BORDER)
    print(table_incompleteness)

    if configurations["print_time"]:
        table_aggregated_time = generate_times_table(time_register, SINGLE_BORDER)
        print(table_aggregated_time)

    print()
