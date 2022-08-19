""" Logging configurations. """

import logging
import os
from datetime import datetime


def initialize_logger():
    """ Initialize OntCatOWL Logger. """

    # Create a custom logger
    new_logger = logging.getLogger("OntCatOWL")
    new_logger.setLevel(logging.DEBUG)

    # Creates a new logger only if OntCatOWL does not exist
    if not logging.getLogger("OntCatOWL").hasHandlers():

        # Creating CONSOLE handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # If directory "/log" does not exist, create it
        log_dir = "log/"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Creating FILE handler
        now = datetime.now()
        date_time = now.strftime("%Y.%m.%d-%H.%M.%S")
        file_handler = logging.FileHandler(f"{log_dir}{date_time}.log")
        file_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        console_format = logging.Formatter('%(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [func: %(funcName)s '
                                        'in %(filename)s]')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        new_logger.addHandler(console_handler)
        new_logger.addHandler(file_handler)

    return new_logger
