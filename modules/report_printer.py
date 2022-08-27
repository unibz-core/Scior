""" Functions for printing in file a report of the current state of the ontology dataclass list in
a readable format. """

import hashlib
import os
from datetime import datetime

from modules.logger_config import initialize_logger


def print_report_file(ontology_dataclass_list):
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

    # Creating report hash
    enc_report = report.encode('utf-8')
    report_hash = hashlib.sha256(enc_report).hexdigest()
    format_report_hash = "CONTENT HASH SHA256 = " + str(report_hash) + "\n\n"

    # Creating report file
    now = datetime.now()
    date_time = now.strftime("%Y.%m.%d-%H.%M.%S")
    with open(f"{report_dir}{date_time}.report", 'w') as f:
        f.write(format_report_hash + report)

    logger.info("Report successfully printed.")
