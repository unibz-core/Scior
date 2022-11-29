""" Functions for printing in file a report of the current state of the ontology dataclass list in
MarkDown format. """
import os

from modules.logger_config import initialize_logger
from modules.report_content import get_content100, get_content200, \
    get_content300_400, get_content500, get_content600
from modules.results_calculation import generate_result_classes_lists
from modules.utils_dataclass import sort_all_ontology_dataclass_list
from modules.utils_general import get_date_time


def print_report_file(ontology_dataclass_list, start_date_time, end_date_time, end_date_time_out, elapsed_time,
                      global_configurations, before_statistics, after_statistics,
                      consolidated_statistics, time_register, restriction):
    """ Printing a file report, in MarkDown syntax, containing the state of the ontology before and after
    the execution of OntCatOWL.

    Restrictions:
        - "PRINT_ALL" - prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    logger = initialize_logger()
    logger.info("Printing report of the current state of the ontology dataclass list using markdown syntax ...")

    sort_all_ontology_dataclass_list(ontology_dataclass_list)

    # If directory "/report" does not exist, create it
    report_dir = "reports/"
    try:
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
    except OSError as error:
        logger.error(f"Could not create {report_dir} directory. Exiting program."
                     f"System error reported: {error}")
        exit(1)

    report_name = f"{report_dir}report-{get_date_time()}.md"

    lists_before, lists_after = generate_result_classes_lists(before_statistics, after_statistics)

    title_000 = "# OntCatOWL Final Results Report\n\n"
    title_100 = "\n## Table of Contents\n\n"
    title_200 = "\n## Execution Information\n\n"
    title_300 = "\n## Lists of Classes Before OntCatOWL\n\n"
    title_400 = "\n## Lists of Classes After OntCatOWL\n\n"
    title_500 = "\n## Results Statistics\n\n"
    title_600 = "\n## Final Classes' Classifications\n\n"

    content_100 = get_content100(restriction)
    content_200 = get_content200(ontology_dataclass_list, report_name, start_date_time, end_date_time,
                                 end_date_time_out,
                                 elapsed_time, time_register, global_configurations)
    content_300 = get_content300_400(lists_before, restriction)
    content_400 = get_content300_400(lists_after, restriction)
    content_500 = get_content500(ontology_dataclass_list, consolidated_statistics, restriction)
    content_600 = get_content600(ontology_dataclass_list, restriction)

    report = title_000 + title_100 + content_100 + title_200 + content_200 + title_300 + content_300 + \
             title_400 + content_400 + title_500 + content_500 + title_600 + content_600

    # Creating report file

    try:
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report successfully printed. Access it in {os.path.abspath(report_name)}.")
    except OSError as error:
        logger.error(f"Could not print report file. Exiting program."
                     f"System error reported: {error}")
        exit(1)
