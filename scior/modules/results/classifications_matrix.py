""" As there are 14 gUFO Endurant Types, The classifications matrix is a 15x15 matrix.
    Each matrix element indicates a QUANTITY of classes.

    The ROWS` index (from 0 to 14) indicates how many known types BEFORE the execution.
    The COLUMNS` index (from 0 to 14) indicates how many known types AFTER the execution.
    The position (ROW, COL) indicates how many classes began with ROW known types and ended with COL known types.

    E.g., if the value 17 is stored in the matrix position (0,5) it indicates that 17 classes started the evaluation
        (i.e., were received as inputs by the user) without known classifications and ended (i.e., were provided
        as outputs by Scior) with 5 known gUFO types.

    Regarding the nomenclature used in the statistics, classes in the:

        - row 0 indicate the amount of TOTALLY UNKNOWN CLASSES in the INPUT
        - rows 1 to 13 indicate the amount of PARTIALLY KNOWN CLASSES in the INPUT
        - row 14 indicate the amount of TOTALLY KNOWN CLASSES in the INPUT

        - column 0 indicate the amount of TOTALLY UNKNOWN CLASSES in the OUTPUT
        - columns 1 to 13 indicate the amount of PARTIALLY KNOWN CLASSES in the OUTPUT
        - column 14 indicate the amount of TOTALLY KNOWN CLASSES in the OUTPUT

    IMPORTANT: CURRENTLY THE CLASSIFICATIONS MATRIX CONTAINS INFORMATION ABOUT TYPES ONLY. INDIVIDUALS ARE OUT OF SCOPE.
    """

from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass

from scior.modules.resources_gufo import GUFO_LIST_ENDURANT_TYPES, GUFO_LIST_LEAF_CLASSIFICATIONS
from scior.modules.utils_dataclass import get_dataclass_by_uri


def generate_empty_matrix(matrix_size: int) -> list[list]:
    """ Creating an empty matrix (i.e., filled with zeros) of size matrix_size x matrix_size.
    The matrix ranges from 0 (inclusive) to matrix_size (inclusive).
    """

    # initializing the classification matrix with zeros
    empty_matrix = []
    for _ in range(0, matrix_size):
        new_line = [0] * matrix_size
        empty_matrix.append(new_line)

    return empty_matrix


def populate_leaves_matrix(leaves_matrix: list[list], before_dataclass_list: list[OntologyDataClass],
                           after_dataclass_list: list[OntologyDataClass]) -> list[list]:
    """ Populates the leaves_matrix (that is received as an argument filled with zeros). """

    for after_dataclass in after_dataclass_list:
        before_dataclass = get_dataclass_by_uri(before_dataclass_list, after_dataclass.uri)

        known_size_b = 0
        known_size_a = 0

        for leaf_classification in GUFO_LIST_LEAF_CLASSIFICATIONS:

            # Calculating known size before and after
            if leaf_classification not in before_dataclass.can_type:
                known_size_b += 1
            if leaf_classification not in after_dataclass.can_type:
                known_size_a += 1

        leaves_matrix[known_size_b][known_size_a] += 1

    return leaves_matrix


def populate_classifications_matrix(classifications_matrix: list[list], before_dataclass_list: list[OntologyDataClass],
                                    after_dataclass_list: list[OntologyDataClass]) -> list[list]:
    """ Populates the classification_matrix (that is received as an argument filled with zeros). """

    for after_dataclass in after_dataclass_list:
        before_dataclass = get_dataclass_by_uri(before_dataclass_list, after_dataclass.uri)

        # Is size must be subtracted by one because of the base class ('EndurantType') which is asserted to all classes
        is_size_b = len(before_dataclass.is_type) - 1
        is_size_a = len(after_dataclass.is_type) - 1

        not_size_b = len(before_dataclass.not_type)
        not_size_a = len(after_dataclass.not_type)

        # Calculating known size
        known_size_b = is_size_b + not_size_b
        known_size_a = is_size_a + not_size_a

        # The corresponding position is added in one (corresponding to one more class in that coordinate)
        classifications_matrix[known_size_b][known_size_a] += 1

    return classifications_matrix


def generate_classifications_matrix(before_dataclass_list: list[OntologyDataClass],

                                    after_dataclass_list: list[OntologyDataClass]) -> tuple[list[list], list[list]]:
    """ Receives 'before' and 'after' lists of ontology dataclasses and creates the classifications matrix. """

    # TOTAL CLASSIFICATIONS' MATRIX

    # Total number of possible classifications (including 0 and excluding 'EndurantType'). Result = 15
    classifications_matrix_size = len(GUFO_LIST_ENDURANT_TYPES)

    # Generating new classifications matrix
    classifications_matrix = generate_empty_matrix(classifications_matrix_size)

    # Populate the classifications matrix
    classifications_matrix = populate_classifications_matrix(classifications_matrix, before_dataclass_list,
                                                             after_dataclass_list)

    # LEAF CLASSIFICATIONS' MATRIX

    # Number of possible leaf classifications (including 0, as there is no). Result = 9
    leaves_matrix_size = len(GUFO_LIST_LEAF_CLASSIFICATIONS) + 1

    # Generating new leaves matrix
    leaves_matrix = generate_empty_matrix(leaves_matrix_size)

    # Populate the classifications matrix
    leaves_matrix = populate_leaves_matrix(leaves_matrix, before_dataclass_list, after_dataclass_list)

    return classifications_matrix, leaves_matrix
