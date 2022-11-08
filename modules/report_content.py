""" Functions that returns the strings to be printed in the Final Results Report. """
from modules.logger_config import initialize_logger
from modules.utils_dataclass import generate_hash_ontology_dataclass_list


def get_content100(restrictions):
    """ Final Results Report - TABLE OF CONTENTS """

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

    if restrictions == "PRINT_ALL" or restrictions == "TYPE_ONLY":
        line_11 = "\t* [Results' Statistics for Types](#results-statistics-for-types)\n"
    else:
        line_11 = ""

    if restrictions == "PRINT_ALL" or restrictions == "INDIVIDUALS_ONLY":
        line_12 = "\t* [Results' Statistics for Individuals]" \
                  "(#results-statistics-for-individuals)\n"
    else:
        line_12 = ""

    if restrictions == "PRINT_ALL" or restrictions == "TOTAL_ONLY":
        line_13 = "\t* [Results' Statistics for Total (Types + Individuals)]" \
                  "(#results-statistics-for-total--types--individuals-)\n"
    else:
        line_13 = ""

    line_14 = "\t* [Final Classes Classifications (IS, CAN, and NOT lists)]" \
              "(#final-classes-classifications--is-can-and-not-lists-)\n"
    line_15 = "\t* [Final Classifications of Partially and Completely Known Classes]" \
              "(#final-classifications-of-partially-and-completely-known-classes)\n"
    line_16 = "\t* [Final Classifications of All Classes](#final-classifications-of-all-classes)\n"

    return_string = line_01 + line_02 + line_03 + line_04 + line_05 + line_06 + line_07 + line_08 + line_09 + line_10 + line_11 + line_12 + line_13 + line_14 + line_15 + line_16

    return return_string


def get_content200(ontology_dataclass_list, start_date_time, end_date_time, end_date_time_out, elapsed_time,
                   configurations):
    """ Presents some information about the software execution."""

    line_01 = f"OntCatOWL successfully performed.\n" \
              f"* Start time {start_date_time}\n" \
              f"* End time {end_date_time}\n" \
              f"* Total elapsed time: {elapsed_time} seconds.\n\n"

    if configurations["is_automatic"]:
        automation_level = "automatic"
    else:
        automation_level = "interactive"
    if configurations["is_complete"]:
        completion = "complete"
    else:
        completion = "incomplete"

    line_02 = f"Configurations:\n" \
              f"* Automation level: {automation_level}\n" \
              f"* Model completion assumption: {completion}\n" \
              f"* Reasoning enabled: {configurations['reasoning']}\n" \
              f"* Execution times printed: {configurations['print_time']}\n" \
              f"* GUFO imported in output: {configurations['import_gufo']}\n\n"

    output_file_name = configurations["ontology_path"][:-4] + "-" + end_date_time_out + ".out.ttl"

    line_03 = f"Processed files:\n" \
              f"* Input ontology file: {configurations['ontology_path']}\n" \
              f"* Output ontology file: {output_file_name}\n" \
              f"* Report file in /report folder\n" \
              f"* Log file in /log folder\n\n"

    hash_types = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "TYPES_ONLY")
    hash_individuals = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "INDIVIDUALS_ONLY")
    hash_total = generate_hash_ontology_dataclass_list(ontology_dataclass_list, "TOTAL")

    line_04 = f"Solution hashes:\n" \
              f"* Hash for types: {hash_types}\n" \
              f"* Hash for individuals: {hash_individuals}\n" \
              f"* Total hash: {hash_total}\n\n"

    return_string = line_01 + line_02 + line_03 + line_04

    return return_string


def get_content300_400(result_lists, restrictions="PRINT_ALL"):
    """ Prints lists of situations. """

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
        title_x10 = f"### List of {result_lists[i].situation} Classes {result_lists[0]} OntCatOWL\n"

        # TU/PK/TK Classes Before/After - Types Only
        if restrictions == "PRINT_ALL" or restrictions == "TYPES_ONLY":
            title_x11 = f"#### {result_lists[i].situation} Classes {result_lists[0]} - Types Only\n"
            for element in result_lists[i].list_uris_types:
                content_x11 += "* " + element + "\n"

        # TU/PK/TK Classes Before/After - Individuals Only
        if restrictions == "PRINT_ALL" or restrictions == "INDIVIDUALS_ONLY":
            title_x12 = f"#### {result_lists[i].situation} Classes {result_lists[0]} - Individuals Only\n"
            for element in result_lists[i].list_uris_individuals:
                content_x12 += "* " + element + "\n"

        # TU/PK/TK Classes Before/After - Total
        if restrictions == "PRINT_ALL" or restrictions == "TOTAL_ONLY":
            title_x13 = f"#### {result_lists[i].situation} Classes {result_lists[0]} - TOTAL (Types + Individuals)\n"
            for element in result_lists[i].list_uris_all:
                content_x13 += "* " + element + "\n"

        content_all += title_x10 + title_x11 + content_x11 + title_x12 + content_x12 + title_x13 + content_x13

    return_string = intro + content_all

    return return_string
