""" Argument Treatments """

import argparse

from modules.logger_config import initialize_logger


def treat_interactivity_level_options(arguments):
    """ Treats argument option for the user's level of interactiveness with OntCatOWL. """

    # Default interactivity value
    interactivity_level = "automatic"

    if arguments.automatic:
        interactivity_level = "automatic"
    else:
        # In case of more than one value for these fields the default values are kept.
        if arguments.always_interactive and arguments.always_automatic:
            interactivity_level = "automatic"
        elif arguments.always_interactive:
            interactivity_level = "always_interactive"
        elif arguments.always_automatic:
            interactivity_level = "always_automatic"

    return interactivity_level


def treat_completeness_options(arguments):
    """ Treats argument option for completeness of the ontology model. """

    if arguments.complete and not arguments.incomplete:
        completeness_option = True
    else:
        completeness_option = False

    return completeness_option


def treat_arguments(software_version):
    """ Treats user input arguments. """

    logger = initialize_logger()
    logger.debug("Parsing arguments...")

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog="OntCatOWL",
                                               usage="ontcatowl.py "
                                                     "[INTERACTIVITY_OPTION] [COMPLETENESS_OPTION] [GENERAL_OPTIONS] "
                                                     "ontology_file",
                                               description="Identification of ontological categories for "
                                                           "OWL ontologies (https://github.com/unibz-core/OntCatOWL/).",
                                               allow_abbrev=False,
                                               epilog="Only one INTERACTIVE_OPTION and "
                                                      "only one COMPLETENESS_OPTION can be chosen. "
                                                      "Default values are -2 and -i, respectively. "
                                                      "In case of invalid or duplicated information, "
                                                      "the default values are kept. ")

    arguments_parser.version = software_version

    # OPTIONAL ARGUMENTS

    # Level of interactiveness arguments
    arguments_parser.add_argument("-1", "--always_interactive", action='store_true',
                                  help="Run in 'Always Interactive' mode. "
                                       "No modifications are performed without the agreement of the user.")

    arguments_parser.add_argument("-2", "--automatic",
                                  action='store_true',
                                  help="(DEFAULT) Run in 'Automatic' mode. "
                                       "Automatic when possible, interactive if necessary.")

    arguments_parser.add_argument("-3", "--always_automatic", action='store_true',
                                  help="Run in 'Always Automatic' mode. "
                                       "Automatic only. No manual intervention is needed.")

    # Ontology completeness arguments
    arguments_parser.add_argument("-c", "--complete", action='store_true',
                                  help="The loaded ontology is a complete model. "
                                       "New classes cannot be created by the user.")

    arguments_parser.add_argument("-i", "--incomplete", action='store_true',
                                  help="(DEFAULT) The loaded ontology is an incomplete model. "
                                       "New classes can be created by the user.")

    # General arguments
    arguments_parser.add_argument("-t", "--times", action='store_true',
                                  help="Prints the execution times of all functions.")

    arguments_parser.add_argument("-p", "--partial", action='store_true',
                                  help="Saves in files the partial ontology and reports before any user interaction.")

    arguments_parser.add_argument("-g", "--gufo", action='store_true',
                                  help="Imports GUFO ontology in the output ontology file.")

    # Automatic arguments
    arguments_parser.add_argument("-v", "--version", action="version", help="Prints the software version and exit.")

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("ontology_file", type=str, action="store", help="The ontology file to be loaded.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    global_configurations = {"partial_results": arguments.partial,
                             "import_gufo": arguments.gufo,
                             "interactivity_level": treat_interactivity_level_options(arguments),
                             "is_complete": treat_completeness_options(arguments),
                             "print_time": arguments.times,
                             "ontology_path": arguments.ontology_file}

    logger.debug(f"Arguments Parsed. Obtained values are: {global_configurations}")

    return global_configurations
