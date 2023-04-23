""" Argument Treatments """

import argparse

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()

def treat_arguments(software_acronym: str, software_name: str, software_version: str, software_url: str) -> dict:
    """ Treat arguments provided by the user when starting software executiong. """

    LOGGER.debug("Parsing arguments...")

    about_message = software_acronym + " - version " + software_version

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog="scior",
                                               description=software_acronym + " - " + software_name,
                                               allow_abbrev=False,
                                               epilog="Asterisks indicate default values. More information at: "
                                                      + software_url)

    arguments_parser.version = about_message

    # AUTOMATION LEVEL ARGUMENTS

    automation_group = arguments_parser.add_mutually_exclusive_group()

    automation_group.add_argument("-i", "--interactive", action='store_true', default=False,
                                  help="Execute automatic rules whenever possible, interactive rules when necessary.")

    automation_group.add_argument("-a", "--automatic", action='store_true', default=True,
                                  help="* Execute only automatic rules. Interactive rules are not performed.")

    # ONTOLOGY COMPLETENESS ARGUMENTS

    completeness_group = arguments_parser.add_mutually_exclusive_group()

    completeness_group.add_argument("-cwa", "--is_cwa", action='store_true', default=False,
                                    help="Operate in Closed-World Assumption (CWA).")

    # Regular Mode: Assume that single instances can be automatically classified.
    completeness_group.add_argument("-owa", "--is_owa", action='store_true', default=True,
                                    help="* Operate in Open-World Assumption (OWA) - Regular Mode.")

    # Light Mode: Single instances cannot be automatically classified.
    completeness_group.add_argument("-owal", "--is_owa_light", action='store_true', default=False,
                                    help="* Operate in Open-World Assumption (OWA) - Light Mode.")

    # VERBOSITY ARGUMENTS

    verbosity_group = arguments_parser.add_mutually_exclusive_group()

    verbosity_group.add_argument("-s", "--silent", action='store_true', default=False,
                                 help="Silent mode. Print only basic execution status information.")

    verbosity_group.add_argument("-r", "--verbose", action='store_true', default=True,
                                 help="* Print basic execution information and results.")

    # REGISTER GUFO IN FILE ARGUMENTS

    gufo_in_file = arguments_parser.add_mutually_exclusive_group()

    gufo_in_file.add_argument("-ng", "--gufo_results", action='store_true', default=True,
                              help="* Write in the output ontology file only the gUFO classifications found.")

    gufo_in_file.add_argument("-ig", "--gufo_import", action='store_true', default=False,
                              help="Import gUFO ontology in the output ontology file.")

    gufo_in_file.add_argument("-wg", "--gufo_write", action='store_true', default=False,
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
        "is_automatic": arguments.automatic,
        "is_interactive": arguments.interactive,

        "is_cwa": arguments.is_cwa,
        "is_owa": arguments.is_owa,
        "is_owa_light": arguments.is_owa_light,

        "gufo_results": arguments.gufo_results,
        "gufo_import": arguments.gufo_import,
        "gufo_write": arguments.gufo_write,

        "is_silent": arguments.silent,
        "is_verbose": arguments.verbose,

        "ontology_path": arguments.ontology_file
    }

    LOGGER.debug(f"Arguments parsed. Obtained values are: {global_configurations}.")

    return global_configurations
