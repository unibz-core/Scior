""" Logging configurations """

import logging
import os
from datetime import datetime


def initialize_logger():
    """ Initialize loggers for OntCatOWL. """

    # Create a custom logger
    new_logger = logging.getLogger("OntCatOWL")
    new_logger.setLevel(logging.DEBUG)

    # Creating CONSOLE handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # If directory "/log" does not exist, create it
    dir = "log/"
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Creating FILE handler
    now = datetime.now()
    date_time = now.strftime("%d%m%Y-%H%M%S")
    # TODO (@pedropaulofb): Verify if directory does not exists and, if so, create it.
    file_handler = logging.FileHandler(f"{dir}{date_time}.log")
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    new_logger.addHandler(console_handler)
    new_logger.addHandler(file_handler)

    return new_logger
