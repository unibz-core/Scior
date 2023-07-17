""" Functions related to the creation of hashes for ontology_dataclasses and for the ontology_dataclass_list. """
import hashlib

from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass


def create_ontology_dataclass_hash(ontology_dataclass: OntologyDataClass) -> str:
    """ Creates a concatenation of all elements from a dataclass to be later used to generate the
    ontology_dataclass_list hash.

    :param ontology_dataclass: Data structure that contains information about the class and its internal lists.
    :type ontology_dataclass: OntologyDataClass
    :return: Internal concatenation of all elements from a dataclass to be used as hash.
    :rtype: str
    """

    partial_is = "IS"
    for classification in ontology_dataclass.is_type:
        partial_is += classification

    partial_can = "CAN"
    for classification in ontology_dataclass.can_type:
        partial_can += classification

    partial_not = "NOT"
    for classification in ontology_dataclass.not_type:
        partial_not += classification

    internal_concatenation = ontology_dataclass.uri + partial_is + partial_can + partial_not

    return internal_concatenation


def create_ontology_dataclass_list_hash(ontology_dataclass_list: list[OntologyDataClass]) -> int:
    """ Calculate an integer hexadecimal SHA256 fixed hash the ontology_dataclass_list.

        This hash must be the same every time the internal elements are the same to be comparable among multiple
        executions of Scior.
    """

    dataclasses_hash = ""

    for ontology_dataclass in ontology_dataclass_list:
        dataclasses_hash += create_ontology_dataclass_hash(ontology_dataclass)

    # Used for generating fix hashes
    encoded_dataclasses_hash = dataclasses_hash.encode('utf-8')
    dataclass_list_hash = int(hashlib.sha256(encoded_dataclasses_hash).hexdigest(), 16)

    return dataclass_list_hash
