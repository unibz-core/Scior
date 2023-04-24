""" Functions for printing in file a report of the current state of the ontology dataclass list in
MarkDown format. """
import os

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.problems_treatment.treat_errors import report_error_io_write
from scior.modules.report_content import get_content100, get_content200, \
    get_content300_400, get_content500, get_content700, get_content600
from scior.modules.results_calculation import generate_result_classes_lists
from scior.modules.utils_dataclass import sort_all_ontology_dataclass_list
from scior.modules.utils_general import create_directory_if_not_exists


def print_report_file(ontology_dataclass_list: list[OntologyDataClass],
                      start_date_time: str, end_date_time: str, elapsed_time: float,
                      before_statistics, after_statistics, consolidated_statistics,
                      restriction: str, software_version: str, knowledge_matrix: str) -> None:
    """ Printing a file report, in MarkDown syntax, containing the state of the ontology before and after
    the execution of Scior.

    Restrictions:
        - "PRINT_ALL" - prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.
    """

    logger = initialize_logger()
    logger.debug("Printing report of the current state of the ontology dataclass list using markdown syntax ...")

    sort_all_ontology_dataclass_list(ontology_dataclass_list)

    # If directory "/report" does not exist, create it
    report_dir = "reports/"
    create_directory_if_not_exists(report_dir)

    report_name = f"{report_dir}report-{end_date_time}.md"

    lists_before, lists_after = generate_result_classes_lists(before_statistics, after_statistics)

    title_000 = "# Scior Final Results Report\n\n"
    title_100 = "\n## Table of Contents\n\n"
    title_200 = "\n## Execution Information\n\n"
    title_300 = "\n## Lists of Classes Before Scior\n\n"
    title_400 = "\n## Lists of Classes After Scior\n\n"
    title_500 = "\n## Results Statistics\n\n"
    title_600 = "\n## Knowledge Matrix\n\n"
    title_700 = "\n## Final Classes' Classifications\n\n"

    content_100 = get_content100(restriction)
    content_200 = get_content200(ontology_dataclass_list, report_name, start_date_time, end_date_time,
                                 elapsed_time, software_version)
    content_300 = get_content300_400(lists_before, restriction)
    content_400 = get_content300_400(lists_after, restriction)
    content_500 = get_content500(ontology_dataclass_list, consolidated_statistics, restriction)
    content_600 = get_content600(knowledge_matrix)
    content_700 = get_content700(ontology_dataclass_list, restriction)

    report = title_000 + title_100 + content_100 + title_200 + content_200 + title_300 + content_300 + \
             title_400 + content_400 + title_500 + content_500 + title_600 + content_600 + title_700 + content_700

    # Creating report file
    try:
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write(report)
    except OSError as error:
        file_description = "report file"
        report_error_io_write(report_name, file_description, error)

    logger.info(f"Report successfully printed. Access it in {os.path.abspath(report_name)}.")
