""" Functions for printing in file a report of the current state of the ontology dataclass list in
a readable format. """

import os
from datetime import datetime

from modules.logger_config import initialize_logger


def print_report_file(ontology_dataclass_list):
    logger = initialize_logger()

    logger.info("Printing report of the current state of the ontology dataclass list...")

    # If directory "/report" does not exist, create it
    report_dir = "report/"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Creating report string
    report = ""
    line_separator = "\n\n"
    list_separator = "\n\t\t"
    for i in range(len(ontology_dataclass_list)):
        name = "URI = " + ontology_dataclass_list[i].uri
        list1 = "is_type = " + str(ontology_dataclass_list[i].is_type)
        list2 = "is_individual" + str(ontology_dataclass_list[i].is_individual)
        list3 = "can_type = " + str(ontology_dataclass_list[i].can_type)
        list4 = "can_individual" + str(ontology_dataclass_list[i].can_individual)
        list5 = "not_type = " + str(ontology_dataclass_list[i].not_type)
        list6 = "not_individual" + str(ontology_dataclass_list[i].not_individual)
        line = name + \
               list_separator + list1 + \
               list_separator + list2 + \
               list_separator + list3 + \
               list_separator + list4 + \
               list_separator + list5 + \
               list_separator + list6 + line_separator
        report += line

    # Creating report file
    now = datetime.now()
    date_time = now.strftime("%Y.%m.%d-%H.%M.%S")
    with open(f"{report_dir}{date_time}.report", 'w') as f:
        f.write(report)
