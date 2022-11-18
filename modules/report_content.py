""" Functions that returns the strings to be printed in the Final Results Report. """
import os

from prettytable import MARKDOWN

from modules.logger_config import initialize_logger
from modules.results_printer import generate_classes_table_to_be_printed, generate_classifications_table_to_be_printed, \
    generate_times_table_to_be_printed
from modules.utils_dataclass import generate_hash_ontology_dataclass_list


def get_content100(restriction="PRINT_ALL"):
    """ Final Results Report - TABLE OF CONTENTS

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    line_01 = "* [Execution Information](#execution-information)\n"
    line_02 = "* [Lists of Classes Before OntCatOWL](#lists-of-classes-before-ontcatowl)\n"
    line_03 = "\t* [List of Totally Unknown Classes Before OntCatOWL]" \
              "(#list-of-totally-unknown-classes-before-ontcatowl)\n"
    line_04 = "\t* [List of Partially Known Classes Before OntCatOWL]" \
              "(#list-of-partially-known-classes-before-ontcatowl)\n"
    line_05 = "\t* [List of Totally Known Classes Before OntCatOWL]" \
              "(#list-of-totally-known-classes-before-ontcatowl)\n"
    line_06 = "* [Lists of Classes After OntCatOWL](#lists-of-classes-after-ontcatowl)\n"
    line_07 = "\t* [List of Totally Unknown Classes After OntCatOWL]" \
              "(#list-of-totally-unknown-classes-after-ontcatowl)\n"
    line_08 = "\t* [List of Partially Known Classes After OntCatOWL]" \
              "(#list-of-partially-known-classes-after-ontcatowl)\n"
    line_09 = "\t* [List of Totally Known Classes After OntCatOWL]" \
              "(#list-of-totally-known-classes-after-ontcatowl)\n"
    line_10 = "* [Results Statistics](#results-statistics)\n"

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        line_11 = "\t* [Statistics of the OntCatOWL execution for TYPES]" \
                  "(#statistics-of-the-ontcatowl-execution-for-types)\n"
    else:
        line_11 = ""

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        line_12 = "\t* [Statistics of the OntCatOWL execution for INDIVIDUALS]" \
                  "(#statistics-of-the-ontcatowl-execution-for-individuals)\n"
    else:
        line_12 = ""

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        line_13 = "\t* [Statistics of the OntCatOWL execution for TYPES and INDIVIDUALS]" \
                  "(#statistics-of-the-ontcatowl-execution-for-types-and-individuals)\n"
    else:
        line_13 = ""

    line_14 = "* [Final Classes' Classifications](#final-classes-classifications)\n"

    return_string = line_01 + line_02 + line_03 + line_04 + line_05 + line_06 + line_07 + line_08 + line_09 + \
                    line_10 + line_11 + line_12 + line_13 + line_14

    return return_string


def get_content200(ontology_dataclass_list, report_name, start_date_time, end_date_time, end_date_time_out,
                   elapsed_time, time_register, configurations):
    """ Presents some information about the software execution."""

    line_01 = f"OntCatOWL successfully performed.\n" \
              f"* Start time {start_date_time}\n" \
              f"* End time {end_date_time}\n" \
              f"* Total elapsed time: {elapsed_time} seconds.\n"

    table_times = generate_times_table_to_be_printed(time_register, MARKDOWN)

    line_02 = f"\nConfigurations:\n" \
              f"* Automatic execution: {not configurations['is_automatic']}\n" \
              f"* Model is complete: {configurations['is_complete']}\n" \
              f"* Reasoning enabled: {configurations['reasoning']}\n" \
              f"* Execution times printed: {configurations['print_time']}\n" \
              f"* GUFO imported in output file: {configurations['import_gufo']}\n" \
              f"* GUFO saved in output file: {configurations['save_gufo']}\n"

    input_file_name_path = os.path.abspath(configurations['ontology_path'])
    output_file_name = configurations["ontology_path"][:-4] + "-" + end_date_time_out + ".out.ttl"
    output_file_name_path = os.path.abspath(output_file_name)
    report_file_name_path = os.path.abspath(report_name)

    line_03 = f"\nProcessed files:\n" \
              f"* Input ontology file:\n\t* {input_file_name_path}\n" \
              f"* Output ontology file:\n\t* {output_file_name_path}\n" \
              f"* Report file:\n\t* {report_file_name_path}\n" \
              f"* Log file in /log folder\n"

    hash_types = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "TYPES_ONLY")
    hash_individuals = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "INDIVIDUALS_ONLY")
    hash_total = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "TOTAL")

    line_04 = f"\nSolution hashes:\n" \
              f"* Hash for types:\n\t* {hash_types}\n" \
              f"* Hash for individuals:\n\t* {hash_individuals}\n" \
              f"* Total hash:\n\t* {hash_total}\n"

    return_string = line_01 + table_times + "\n" + line_02 + line_03 + line_04

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
        intro = "This section presents the categorization of the classes inputted to OntCatOWL " \
                "(i.e., before its rules' executions) in three lists: Totally Unknown Classes, " \
                "Partially Known Classes, and Totally Known Classes.\n"
    elif result_lists[0] == "After":
        intro = "This section presents the categorization of the classes after processed by OntCatOWL " \
                "(i.e., after its rules' executions) in three lists: Totally Unknown Classes, " \
                "Partially Known Classes, and Totally Known Classes.\n"
    else:
        logger.error("Unexpected list situation. Program aborted.")
        exit(1)

    content_all = ""

    for i in range(1, 4):

        title_x11 = ""
        title_x12 = ""
        title_x13 = ""
        content_x11 = ""
        content_x12 = ""
        content_x13 = ""

        # List of TU/PK/TK Classes Before/After OntCatOWL
        title_x10 = f"\n### List of {result_lists[i].situation} Classes {result_lists[0]} OntCatOWL\n\n"

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
            title_x13 = f"\n#### {result_lists[i].situation} Classes {result_lists[0]} - TOTAL (Types + Individuals)\n\n"
            for element in result_lists[i].list_uris_all:
                content_x13 += "* " + element + "\n"

        content_all += title_x10 + title_x11 + content_x11 + title_x12 + content_x12 + title_x13 + content_x13

    return_string = intro + content_all

    return return_string


def get_content500(list_values_classes, list_values_classifications, restriction="PRINT_ALL"):
    """ Prints statistics for classes and classifications.

    Allowed restriction values:
        - "PRINT_ALL" - (DEFAULT) prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    intro = "This section presents statistics of the execution of OntCatOWL considering classes and " \
            "possible classifications (gUFO elements).\n"

    title_501 = ""
    content_501 = ""
    title_502 = ""
    content_502 = ""
    title_503 = ""
    content_503 = ""

    if restriction == "PRINT_ALL" or restriction == "TYPES_ONLY":
        title_501 = "\n### Statistics of the OntCatOWL execution for TYPES"

        table_classes_types = generate_classes_table_to_be_printed(list_values_classes, "types", MARKDOWN)
        table_classifications_types = generate_classifications_table_to_be_printed(list_values_classifications, "types",
                                                                                   MARKDOWN)

        content_501 = "\n" + table_classes_types + "\n" + table_classifications_types + "\n"

    if restriction == "PRINT_ALL" or restriction == "INDIVIDUALS_ONLY":
        title_502 = "\n### Statistics of the OntCatOWL execution for INDIVIDUALS"

        table_classes_individuals = generate_classes_table_to_be_printed(list_values_classes, "individuals",
                                                                         MARKDOWN)
        table_classifications_individuals = generate_classifications_table_to_be_printed(list_values_classifications,
                                                                                         "individuals", MARKDOWN)

        content_502 = "\n" + table_classes_individuals + "\n" + table_classifications_individuals + "\n"

    if restriction == "PRINT_ALL" or restriction == "TOTAL_ONLY":
        title_503 = "\n### Statistics of the OntCatOWL execution for TYPES and INDIVIDUALS"

        table_classes_total = generate_classes_table_to_be_printed(list_values_classes, "total", MARKDOWN)
        table_classifications_total = generate_classifications_table_to_be_printed(list_values_classifications, "total",
                                                                                   MARKDOWN)

        content_503 = "\n" + table_classes_total + "\n" + table_classifications_total + "\n"

    content_all = title_501 + content_501 + title_502 + content_502 + title_503 + content_503

    return_string = intro + content_all

    return return_string


def get_content600(ontology_dataclass_list, restriction="PRINT_ALL"):
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
        logger.error("Restriction unknown. Program aborted.")
        exit(1)

    return class_print_information
