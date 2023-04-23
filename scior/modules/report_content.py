""" Functions that returns the strings to be printed in the Final Results Report. """
import inspect
import os

from prettytable import MARKDOWN, PrettyTable

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_hashing import create_ontology_dataclass_list_hash
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.results_printer import generate_classes_table, generate_classifications_table, \
    generate_times_table, generate_incompleteness_table
from scior.modules.utils_general import get_computer_specifications


def get_content100(restriction="PRINT_ALL"):
    """ Final Results Report - TABLE OF CONTENTS

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    line_01 = "* [Execution Information](#execution-information)\n"
    line_02 = "* [Lists of Classes Before Scior](#lists-of-classes-before-scior)\n"
    line_03 = "\t* [List of Totally Unknown Classes Before Scior]" \
              "(#list-of-totally-unknown-classes-before-scior)\n"
    line_04 = "\t* [List of Partially Known Classes Before Scior]" \
              "(#list-of-partially-known-classes-before-scior)\n"
    line_05 = "\t* [List of Totally Known Classes Before Scior]" \
              "(#list-of-totally-known-classes-before-scior)\n"
    line_06 = "* [Lists of Classes After Scior](#lists-of-classes-after-scior)\n"
    line_07 = "\t* [List of Totally Unknown Classes After Scior]" \
              "(#list-of-totally-unknown-classes-after-scior)\n"
    line_08 = "\t* [List of Partially Known Classes After Scior]" \
              "(#list-of-partially-known-classes-after-scior)\n"
    line_09 = "\t* [List of Totally Known Classes After Scior]" \
              "(#list-of-totally-known-classes-after-scior)\n"
    line_10 = "* [Results Statistics](#results-statistics)\n"

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        line_11 = "\t* [Statistics of the Scior execution for TYPES]" \
                  "(#statistics-of-the-scior-execution-for-types)\n"
    else:
        line_11 = ""

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        line_12 = "\t* [Statistics of the Scior execution for INDIVIDUALS]" \
                  "(#statistics-of-the-scior-execution-for-individuals)\n"
    else:
        line_12 = ""

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        line_13 = "\t* [Statistics of the Scior execution for TYPES and INDIVIDUALS]" \
                  "(#statistics-of-the-scior-execution-for-types-and-individuals)\n"
    else:
        line_13 = ""

    line_14 = "* [Incomplete Classes Identified](#incomplete-classes-identified)\n"

    line_15 = "* [Knowledge Matrix](#knowledge-matrix)\n"

    line_16 = "* [Final Classes' Classifications](#final-classes-classifications)\n"

    return_string = line_01 + line_02 + line_03 + line_04 + line_05 + line_06 + line_07 + line_08 + line_09 + \
                    line_10 + line_11 + line_12 + line_13 + line_14 + line_15 + line_16

    return return_string


def get_content200(ontology_dataclass_list, report_name, start_date_time, end_date_time,
                   elapsed_time, time_register, configurations, software_version):
    """ Presents some information about the software execution."""

    line_01 = f"Scior version {software_version} successfully performed.\n" \
              f"* Start time {start_date_time}\n" \
              f"* End time {end_date_time}\n" \
              f"* Total elapsed time: {elapsed_time} seconds.\n"

    table_times = generate_times_table(time_register, MARKDOWN)

    computer_specs = get_computer_specifications()

    line_01_specs = f"\nComputer specifications:\n"
    for key in computer_specs.keys():
        line_01_specs += f"* {key}: {computer_specs[key]}\n"

    line_02 = f"\nConfigurations:\n" \
              f"* Automatic execution: {configurations['is_automatic']}\n" \
              f"* Model is complete: {configurations['is_complete']}\n" \
              f"* Execution times printed: {configurations['print_time']}\n" \
              f"* GUFO imported in output file: {configurations['import_gufo']}\n" \
              f"* GUFO saved in output file: {configurations['save_gufo']}\n"

    in_out_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    input_file_name = in_out_file_path + "\\" + configurations["ontology_path"]
    output_file_name = in_out_file_path + "\\" + \
                       os.path.splitext(configurations["ontology_path"])[0] + \
                       "-" + end_date_time + ".out.ttl"

    path_input_file = os.path.abspath(input_file_name)
    path_output_file = os.path.abspath(output_file_name)

    report_file_name_path = os.path.abspath(report_name)

    line_03 = f"\nProcessed files:\n" \
              f"* Input ontology file:\n\t* {path_input_file}\n" \
              f"* Output ontology file:\n\t* {path_output_file}\n" \
              f"* Report file:\n\t* {report_file_name_path}\n" \
              f"* Log file available at '\\log' folder\n"

    hash_types = create_ontology_dataclass_list_hash(ontology_dataclass_list)
    hash_individuals = create_ontology_dataclass_list_hash(ontology_dataclass_list)
    hash_total = create_ontology_dataclass_list_hash(ontology_dataclass_list)

    line_04 = f"\nSolution hashes:\n" \
              f"* Hash for types:\n\t* {hash_types}\n" \
              f"* Hash for individuals:\n\t* {hash_individuals}\n" \
              f"* Total hash:\n\t* {hash_total}\n"

    return_string = line_01 + table_times + "\n" + line_01_specs + line_02 + line_03 + line_04

    return return_string


def get_content300_400(result_lists, restriction="PRINT_ALL"):
    """ Prints lists of situations.

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    """

    logger = initialize_logger()
    intro = ""

    if result_lists[0] == "Before":
        intro = "This section presents the categorization of the classes inputted to Scior " \
                "(i.e., before its rules' executions) in three lists: Totally Unknown Classes, " \
                "Partially Known Classes, and Totally Known Classes.\n"
    elif result_lists[0] == "After":
        intro = "This section presents the categorization of the classes after processed by Scior " \
                "(i.e., after its rules' executions) in three lists: Totally Unknown Classes, " \
                "Partially Known Classes, and Totally Known Classes.\n"
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(result_lists[0], current_function)

    content_all = ""

    for i in range(1, 4):

        title_x11 = ""
        title_x12 = ""
        title_x13 = ""
        content_x11 = ""
        content_x12 = ""
        content_x13 = ""

        # List of TU/PK/TK Classes Before/After Scior
        title_x10 = f"\n### List of {result_lists[i].situation} Classes {result_lists[0]} Scior\n\n"

        # TU/PK/TK Classes Before/After - Types Only
        if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
            title_x11 = f"\n#### {result_lists[i].situation} Classes {result_lists[0]} - Types Only\n\n"
            for element in result_lists[i].list_uris_types:
                content_x11 += "* " + element + "\n"

        # TU/PK/TK Classes Before/After - Individuals Only
        if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
            title_x12 = f"\n#### {result_lists[i].situation} Classes {result_lists[0]} - Individuals Only\n\n"
            for element in result_lists[i].list_uris_individuals:
                content_x12 += "* " + element + "\n"

        # TU/PK/TK Classes Before/After - Total
        if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
            title_x13 = f"\n#### {result_lists[i].situation} Classes {result_lists[0]} - " \
                        f"TOTAL (Types + Individuals)\n\n"
            for element in result_lists[i].list_uris_all:
                content_x13 += "* " + element + "\n"

        content_all += title_x10 + title_x11 + content_x11 + title_x12 + content_x12 + title_x13 + content_x13

    return_string = intro + content_all

    return return_string


def get_content500(ontology_dataclass_list, consolidated_statistics, restriction="PRINT_ALL"):
    """ Prints statistics for classes and classifications.

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    intro = "This section presents statistics of the execution of Scior considering classes and " \
            "possible classifications (gUFO elements).\n"

    title_501 = ""
    content_501 = ""
    title_502 = ""
    content_502 = ""
    title_503 = ""
    content_503 = ""

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        title_501 = "\n### Statistics of the Scior execution for TYPES"

        table_classes_types = generate_classes_table(consolidated_statistics, "types", MARKDOWN)
        table_classifications_types = generate_classifications_table(consolidated_statistics, "types",
                                                                     MARKDOWN)

        content_501 = "\n" + table_classes_types + "\n" + table_classifications_types + "\n"

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        title_502 = "\n### Statistics of the Scior execution for INDIVIDUALS"

        table_classes_individuals = generate_classes_table(consolidated_statistics, "individuals",
                                                           MARKDOWN)
        table_classifications_individuals = generate_classifications_table(consolidated_statistics,
                                                                           "individuals", MARKDOWN)

        content_502 = "\n" + table_classes_individuals + "\n" + table_classifications_individuals + "\n"

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        title_503 = "\n### Statistics of the Scior execution for TYPES and INDIVIDUALS"

        table_classes_total = generate_classes_table(consolidated_statistics, "total", MARKDOWN)
        table_classifications_total = generate_classifications_table(consolidated_statistics, "total",
                                                                     MARKDOWN)

        content_503 = "\n" + table_classes_total + "\n" + table_classifications_total + "\n"

    title_504 = "\n## Incomplete Classes Identified"

    table_incompleteness = generate_incompleteness_table(ontology_dataclass_list, MARKDOWN)

    content_504 = "\n" + table_incompleteness + "\n"

    content_all = title_501 + content_501 + title_502 + content_502 + title_503 + content_503 + title_504 + content_504

    return_string = intro + content_all

    return return_string


def get_content600(knowledge_matrix):
    """ Prints the knowledge matrix using pretty tables. """

    intro = "The Knowledge Matrix presents how much knowledge were discovered. The position (ROW, COL) indicates " \
            "how many classes began with ROW known types (i.e., positive or negative classifications) and ended with " \
            "COL known types.\n\n"

    columns_titles = []

    # Adding titles of columns' 1 to 15
    for i in range(0, 15):
        columns_titles.append("A" + str(i))

    pretty_table = PrettyTable(columns_titles)

    pretty_table.add_rows(knowledge_matrix)

    # Adding column 0 titles
    first_row_name = "B\\A"
    pretty_table._field_names.insert(0, first_row_name)
    pretty_table._align[first_row_name] = 'c'
    pretty_table._valign[first_row_name] = 't'
    for i, _ in enumerate(pretty_table._rows):
        pretty_table._rows[i].insert(0, "B" + str(i))

    pretty_table.align = "c"
    pretty_table.set_style(MARKDOWN)

    table_text = pretty_table.get_string()
    return_string = intro + table_text

    return return_string


def get_content700(ontology_dataclass_list, restriction="PRINT_ALL"):
    """ Prints final lists of classes according to the received restriction.

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    logger = initialize_logger()

    class_print_information = ""

    if restriction == "TYPES_ONLY":

        for dataclass in ontology_dataclass_list:
            class_print_information += f"\n* `Class URI` = {dataclass.uri}\n\n" \
                                       f"\t* `is_type`\t\t=\t{dataclass.is_type}\n" \
                                       f"\t* `can_type`\t=\t{dataclass.can_type}\n" \
                                       f"\t* `not_type`\t=\t{dataclass.not_type}\n"

    elif restriction == "INDIVIDUALS_ONLY":

        for dataclass in ontology_dataclass_list:
            class_print_information += f"\n* `Class URI` = {dataclass.uri}\n\n" \
                                       f"\t* `is_individual`\t=\t{dataclass.is_individual}\n" \
                                       f"\t* `can_individual`\t=\t{dataclass.can_individual}\n" \
                                       f"\t* `not_individual`\t=\t{dataclass.not_individual}\n"

    elif restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":

        for dataclass in ontology_dataclass_list:
            class_print_information += f"\n* `Class URI` = {dataclass.uri}\n\n" \
                                       f"\t* `is_type`\t\t\t=\t{dataclass.is_type}\n" \
                                       f"\t* `is_individual`\t=\t{dataclass.is_individual}\n" \
                                       f"\t* `can_type`\t\t=\t{dataclass.can_type}\n" \
                                       f"\t* `can_individual`\t=\t{dataclass.can_individual}\n" \
                                       f"\t* `not_type`\t\t=\t{dataclass.not_type}\n" \
                                       f"\t* `not_individual`\t=\t{dataclass.not_individual}\n"
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(restriction, current_function)

    return class_print_information
