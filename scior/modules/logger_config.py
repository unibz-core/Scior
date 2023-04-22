""" Logging configurations. """
import logging

from scior.modules.utils_general import get_date_time, create_directory_if_not_exists


def initialize_logger(caller: str = "Scior") -> logging.Logger:
    """ Create and Initialize Scior Logger.
        Parameter caller informs which function is creating the logger. Valid values are Scior and Scior-Tester.
        The created logger is called 'execution-logger'.
    """

    # Create a custom logger
    new_logger = logging.getLogger("execution-logger")

    # Creates a new logger only if Scior does not exist
    if not logging.getLogger("Logger").hasHandlers():

        # Creating CONSOLE and FILE handlers
        console_handler = logging.StreamHandler()
        if caller == "Scior":
            console_handler.setLevel(logging.INFO)
        elif caller == "Scior-Tester":
            console_handler.setLevel(logging.ERROR)
        else:
            raise ValueError(f"Logger parameter unknown ({caller}). Aborting execution.")

        # If directory "/log" does not exist, create it
        log_directory = "logs/"
        create_directory_if_not_exists(log_directory)

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
