""" Logging configurations. """
import logging
import os

from scior.modules.utils_general import get_date_time


def initialize_logger(caller: str = "Scior") -> logging.Logger:
    """ Create and Initialize Scior Logger.
        Parameter caller informs which function is creating the logger. Valid values are Scior and Scior-Tester.
        The created logger is called 'execution-logger'.
    """

    # Create a custom logger
    new_logger = logging.getLogger("execution-logger")

    # Setting lower level levels
    if caller == "Scior":
        new_logger.setLevel(logging.DEBUG)
    elif caller == "Scior-Tester":
        new_logger.setLevel(logging.ERROR)
    else:
        raise ValueError(f"Logger parameter unknown ({caller}). Aborting execution.")

    # Creates a new logger only if Scior does not exist
    if not logging.getLogger("execution-logger").hasHandlers():

        # Creating CONSOLE handlers
        console_handler = logging.StreamHandler()
        if caller == "Scior":
            console_handler.setLevel(logging.INFO)
        elif caller == "Scior-Tester":
            console_handler.setLevel(logging.ERROR)

        # If directory "/log" does not exist, create it
        # IMPORTANT: do not substitute because of circular dependency.
        log_directory = "logs/"
        try:
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
        except OSError as error:
            print(f"Could not create log directory {log_directory}. Program aborted.")
            raise OSError(error)

        # Creating FILE handler
        file_handler = logging.FileHandler(f"{log_directory}{get_date_time()}.log")
        if caller == "Scior":
            file_handler.setLevel(logging.DEBUG)
        elif caller == "Scior-Tester":
            file_handler.setLevel(logging.ERROR)

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
