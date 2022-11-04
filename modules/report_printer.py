""" Functions for printing in file a report of the current state of the ontology dataclass list in
MarkDown format. """

import os

from modules.logger_config import initialize_logger
from modules.report_content import get_content100, get_content200, \
    get_content300_400
from modules.results_calculation import generate_result_classes_lists
from modules.utils_general import get_date_time


def print_report_file(before_statistics, after_statistics, restrictions):
    """ Printing a file report, in MarkDown syntax, containing the state of the ontology before and after
    the execution of OntCatOWL.

    Restrictions:
        - "PRINT_ALL" - prints types, individuals, and total tables.
        - "TYPES_ONLY" - prints only types table.
        - "INDIVIDUALS_ONLY" - prints only individuals table.
        - "TOTAL_ONLY" - prints only total table.

    REPORT STRUCTURE:
    # Title
        ## Table of Contents (with links)
        ## Execution Information (numbers, hash, etc.)
        ## Lists of Classes Before OntCatOWL
            ### List Totally Unknown Classes Before OntCatOWL
            ### List Partially Known Classes Before OntCatOWL
            ### List Totally Known Classes Before OntCatOWL
        ## Lists of Classes After OntCatOWL
            ### List Totally Unknown Classes After OntCatOWL
            ### List Partially Known Classes After OntCatOWL
            ### List Totally Known Classes After OntCatOWL
        ## Results Statistics
            ### Results Statistics for Types
            ### Results Statistics for Individuals
            ### Results Statistics for Total (Types + Individuals)
        ## Final Classes Classifications (IS, CAN, and NOT lists)
            ### Partially and Completely Known Classes
            ### All Classes
    """

    logger = initialize_logger()
    logger.info("Printing report of the current state of the ontology dataclass list using markdown syntax ...")

    # If directory "/report" does not exist, create it
    report_dir = "reports/"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    lists_before, lists_after = generate_result_classes_lists(before_statistics, after_statistics)

    title_000 = "# OntCatOWL Final Results Report\n"
    title_100 = "## Table of Contents\n"
    title_200 = "## Execution Information\n"
    title_300 = "## Lists of Classes Before OntCatOWL\n"
    title_400 = "## Lists of Classes After OntCatOWL\n"
    title_500 = "## Results Statistics\n"
    title_510 = "### Results' Statistics for Types\n"
    title_520 = "### Results' Statistics for Individuals\n"
    title_530 = "### Results' Statistics for Total (Types + Individuals)\n"
    title_600 = "## Final Classes Classifications (IS, CAN, and NOT lists)\n"
    title_610 = "### Final Classifications of Partially and Completely Known Classes\n"
    title_620 = "### Final Classifications of All Classes\n"

    content_100 = get_content100(restrictions)
    content_200 = get_content200()  # TO BE DONE
    content_300 = get_content300_400(lists_before, restrictions)
    content_400 = get_content300_400(lists_after, restrictions)
    # content_41 = get_content41()
    # content_42 = get_content42()
    # content_43 = get_content43()
    # content_5 = get_content5()
    # content_51 = get_content51()
    # content_52 = get_content52()
    # content_53 = get_content53()
    # content_6 = get_content6()
    # content_61 = get_content61()
    # content_62 = get_content62()
    #
    report = title_000 + title_100 + content_100 + title_200 + content_200 + title_300 + content_300 + title_400 + content_400

    # # Creating hash
    # enc_report = report.encode('utf-8')
    # report_hash = hashlib.sha256(enc_report).hexdigest()
    # format_report_hash = "CONTENT HASH SHA256 = " + str(report_hash) + "\n\n"

    # Creating report file
    with open(f"{report_dir}{get_date_time()}.md", 'w') as f:
        f.write(report)

    logger.info("Report successfully printed.")
