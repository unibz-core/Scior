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

    # OPTIONAL ARGUMENTS

    # Automation level

    automation_group = arguments_parser.add_mutually_exclusive_group()

    automation_group.add_argument("-i", "--interactive", action='store_true',
                                  help="Execute automatic rules whenever possible. "
                                       "Execute interactive rules only if necessary (default).")

    automation_group.add_argument("-a", "--automatic",
                                  action='store_true',
                                  help="Execute only automatic rules. Interactive rules are not performed.")

    # Ontology completeness arguments

    completeness_group = arguments_parser.add_mutually_exclusive_group()

    completeness_group.add_argument("-owa", "--adopt_owa", action='store_true',
                                    help="Operate in Open-World Assumption (OWA) (default).")

    completeness_group.add_argument("-cwa", "--adopt_cwa", action='store_true',
                                    help="Operate in Closed-World Assumption (CWA).")

    # Verbosity arguments

    # v0: print only start and end information and errors
    # v1: v0 + logger information (default)
    # v2: v1 + incompleteness cases found (logger warnings)
    # v3: print all logger messages, including debbugging messages

    # General arguments
    arguments_parser.add_argument("-t", "--times", action='store_true',
                                  help="Print on the screen the execution times of all functions.")

    arguments_parser.add_argument("-g1", "--gufo1", action='store_true',
                                  help="Import gUFO ontology in the output ontology file.")

    arguments_parser.add_argument("-g2", "--gufo2", action='store_true',
                                  help="Save all gUFO statements in the output ontology file.")

    # Automatic arguments
    arguments_parser.add_argument("-v", "--version", action="version", help="Print the software version and exit.")

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("ontology_file", type=str, action="store", help="The path of the ontology file to "
                                                                                  "be loaded.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    global_configurations = {"import_gufo": arguments.gufo1,
                             "save_gufo": arguments.gufo2,
                             "is_automatic": arguments.automatic,
                             "is_owa": arguments.adopt_owa,
                             "is_cwa": arguments.adopt_cwa,
                             "print_time": arguments.times,
                             "ontology_path": arguments.ontology_file}

    logger.debug(f"Arguments Parsed. Obtained values are: {global_configurations}")

    return global_configurations
