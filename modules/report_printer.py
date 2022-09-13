""" Functions for printing in file a report of the current state of the ontology dataclass list in
a readable format. """

import hashlib
import os
from datetime import datetime

from prettytable import PrettyTable

from modules.logger_config import initialize_logger

SECTION_SEPARATOR = "\n##########################################################\n"

# TODO (@pedropaulofb): These constants have to be updated for using "full GUFO".
NUMBER_GUFO_CLASSES_TYPES = 14
NUMBER_GUFO_CLASSES_INDIVIDUALS = 13
NUMBER_GUFO_CLASSES = NUMBER_GUFO_CLASSES_TYPES + NUMBER_GUFO_CLASSES_INDIVIDUALS


def print_report_file(ontology_dataclass_list, nodes_list):
    """ printing in file a report of the current state of the ontology dataclass list in a readable format."""

    logger = initialize_logger()
    logger.info("Printing report of the current state of the ontology dataclass list...")

    # If directory "/report" does not exist, create it
    report_dir = "report/"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Sorting alphabetically the dataclass list

    ordered_list_uri = []

    for ontology_dataclass in ontology_dataclass_list:
        ordered_list_uri.append(ontology_dataclass.uri)

    ordered_list_uri.sort()

    # Creating report string with alphabetically ordered elements
    report = ""
    line_separator = "\n\n"
    list_separator = "\n\t\t"

    for ordered_uri in ordered_list_uri:
        for ont_dataclass in ontology_dataclass_list:
            if ordered_uri == ont_dataclass.uri:
                name = "URI = " + ont_dataclass.uri
                list1 = "is_type = " + str(ont_dataclass.is_type)
                list2 = "is_individual = " + str(ont_dataclass.is_individual)
                list3 = "can_type = " + str(ont_dataclass.can_type)
                list4 = "can_individual = " + str(ont_dataclass.can_individual)
                list5 = "not_type = " + str(ont_dataclass.not_type)
                list6 = "not_individual = " + str(ont_dataclass.not_individual)
                line = name + \
                       list_separator + list1 + \
                       list_separator + list2 + \
                       list_separator + list3 + \
                       list_separator + list4 + \
                       list_separator + list5 + \
                       list_separator + list6 + line_separator
                report += line

    # Creating hash
    enc_report = report.encode('utf-8')
    report_hash = hashlib.sha256(enc_report).hexdigest()
    format_report_hash = "CONTENT HASH SHA256 = " + str(report_hash) + "\n\n"

    # Creating summary
    print_class_summary(ontology_dataclass_list, nodes_list)

    # Creating report file
    now = datetime.now()
    date_time = now.strftime("%Y.%m.%d-%H.%M.%S")
    with open(f"{report_dir}{date_time}.report", 'w') as f:
        f.write(format_report_hash + report)

    logger.info("Report successfully printed.")


def print_class_summary(ontology_dataclass_list, nodes_list):
    """ Prints evaluation metrics. """

    section_title = "\t\tONTOLOGICAL CLASSIFICATION SUMMARY\t\t"

    total_number_of_classes = len(nodes_list["all"])

    solved_types = 0
    solved_individuals = 0
    solved_total = 0

    reduced_types = 0
    reduced_individuals = 0
    reduced_total = 0

    for ontology_dataclass in ontology_dataclass_list:

        # Calculating TYPES data
        if len(ontology_dataclass.can_type) == 0:
            solved_types += 1
        elif len(ontology_dataclass.can_type) < NUMBER_GUFO_CLASSES_TYPES:
            reduced_types += 1

        # Calculating INDIVIDUALS data
        if len(ontology_dataclass.can_individual) == 0:
            solved_individuals += 1
        elif len(ontology_dataclass.can_individual) < NUMBER_GUFO_CLASSES_INDIVIDUALS:
            reduced_individuals += 1

        # Calculating TOTAL data
        changes = len(ontology_dataclass.can_type) + len(ontology_dataclass.can_individual)
        if changes == 0:
            solved_total += 1
        elif changes < NUMBER_GUFO_CLASSES:
            reduced_total += 1

    improved_types = solved_types + reduced_types

    solved_types_percentage = round(100 * solved_types / total_number_of_classes, 2)
    reduced_types_percentage = round(100 * reduced_types / total_number_of_classes, 2)
    improved_types_percentage: float = round(100 * improved_types / total_number_of_classes, 2)

    improved_individuals = solved_individuals + reduced_individuals

    solved_individuals_percentage = round(100 * solved_individuals / total_number_of_classes, 2)
    reduced_individuals_percentage = round(100 * reduced_individuals / total_number_of_classes, 2)
    improved_individuals_percentage: float = round(100 * improved_individuals / total_number_of_classes, 2)

    improved_total = solved_total + reduced_total

    solved_total_percentage: float = round(100 * solved_total / total_number_of_classes, 2)
    reduced_total_percentage: float = round(100 * reduced_total / total_number_of_classes, 2)
    improved_total_percentage: float = round(100 * improved_total / total_number_of_classes, 2)

    table = PrettyTable(["GROUP", "ITEM", "VALUE", "PERCENTAGE"])

    table.add_row(["Type", "Inputted", total_number_of_classes, 100.0])
    table.add_row(["Type", "Solved", solved_types, solved_types_percentage])
    table.add_row(["Type", "Reduced", reduced_types, reduced_types_percentage])
    table.add_row(["Type", "Improved", improved_types, improved_types_percentage])
    table.add_row(["Type", "Not Improved", improved_types, round(100 - improved_types_percentage, 2)])
    table.add_row(["-----", "-----", "-----", "-----"])

    table.add_row(["Individual", "Inputted", total_number_of_classes, 100.0])
    table.add_row(["Individual", "Solved", solved_individuals, solved_individuals_percentage])
    table.add_row(["Individual", "Reduced", reduced_individuals, reduced_individuals_percentage])
    table.add_row(["Individual", "Improved", improved_individuals, improved_individuals_percentage])
    table.add_row(["-----", "-----", "-----", "-----"])

    table.add_row(["Total", "Inputted", total_number_of_classes, 100.0])
    table.add_row(["Total", "Solved", solved_total, solved_total_percentage])
    table.add_row(["Total", "Reduced", reduced_total, reduced_total_percentage])
    table.add_row(["Total", "Improved", improved_total, improved_total_percentage])

    table.align["GROUP"] = "l"
    table.align["ITEM"] = "l"
    table.align["VALUE"] = "c"
    table.align["PERCENTAGE"] = "c"

    print(SECTION_SEPARATOR + section_title + SECTION_SEPARATOR)
    print(table)
    print(SECTION_SEPARATOR)
