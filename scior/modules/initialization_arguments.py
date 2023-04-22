""" Argument Treatments """

import argparse

from scior.modules.logger_config import initialize_logger


def treat_arguments(software_acronym, software_name, software_version, software_url):
    """ Treats user ontologies arguments. """

    logger = initialize_logger()
    logger.debug("Parsing arguments...")

    about_message = software_acronym + " - version " + software_version

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog="scior",
                                               description=software_acronym + " - " + software_name,
                                               allow_abbrev=False,
                                               epilog=software_url)

    arguments_parser.version = about_message

    # AUTOMATION LEVEL ARGUMENTS

    automation_group = arguments_parser.add_mutually_exclusive_group()

    automation_group.add_argument("-i", "--interactive", action='store_true',
                                  help="Execute automatic rules whenever possible, interactive rules when necessary.")

    automation_group.add_argument("-a", "--automatic", action='store_true',
                                  help="* Execute only automatic rules. Interactive rules are not performed.")

    # ONTOLOGY COMPLETENESS ARGUMENTS

    completeness_group = arguments_parser.add_mutually_exclusive_group()

    completeness_group.add_argument("-owa", "--is_owa", action='store_true',
                                    help="* Operate in Open-World Assumption (OWA).")

    completeness_group.add_argument("-cwa", "--is_cwa", action='store_true',
                                    help="Operate in Closed-World Assumption (CWA).")

    # VERBOSITY ARGUMENTS

    verbosity_group = arguments_parser.add_mutually_exclusive_group()

    verbosity_group.add_argument("-v0", "--verbosity0", action='store_true',
                                 help="Restrict printed information to start, stop, and errors.")

    verbosity_group.add_argument("-v1", "--verbosity1", action='store_true',
                                 help="* Print basic execution status information.")

    verbosity_group.add_argument("-v2", "--verbosity2", action='store_true',
                                 help="Print additional information like incompleteness cases found.")

    # REGISTER GUFO IN FILE ARGUMENTS

    gufo_in_file = arguments_parser.add_mutually_exclusive_group()

    gufo_in_file.add_argument("-ng", "--gufo_classifications", action='store_true',
                              help="* Write in the output ontology file only gUFO classifications found.")

    gufo_in_file.add_argument("-ig", "--gufo_import", action='store_true',
                              help="Import gUFO ontology in the output ontology file.")

    gufo_in_file.add_argument("-wg", "--gufo_write", action='store_true',
                              help="Write all gUFO statements in the output ontology file.")

    # AUTOMATIC ARGUMENTS
    arguments_parser.add_argument("-v", "--version", action="version",
                                  help="Print the software version and exit.")

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("ontology_file", type=str, action="store",
                                  help="The path of the ontology file to be loaded.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    global_configurations = {
        "classifications_gufo": arguments.import_gufo,
        "import_gufo": arguments.import_gufo,
        "save_gufo": arguments.write_gufo,

        "is_automatic": arguments.automatic,
        "is_manual": arguments.manual,

        "is_owa": arguments.is_owa,
        "is_cwa": arguments.is_cwa,

        "print_basic": arguments.is_v0,
        "print_default": arguments.is_v1,
        "print_all": arguments.is_v2,

        "gufo_classifications": arguments.gufo_classifications,
        "gufo_import": arguments.gufo_import,
        "gufo_write": arguments.gufo_write,

        "ontology_path": arguments.ontology_file
    }

    logger.debug(f"Arguments Parsed. Obtained values are: {global_configurations}")

    return global_configurations
