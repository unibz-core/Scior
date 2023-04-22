""" Implementation of caller/switcher for rules of group AUX. """
from rdflib import URIRef, RDFS, Graph

from scior.modules.logger_config import initialize_logger

SCIOR_NAMESPACE = "https://purl.org/scior/"
LOGGER = initialize_logger()


def run_ir36(ontology_graph: Graph) -> None:
    """ Executes rule IR36 from group AUX.

    Code: IR36
    Definition: Kind(z) ^ subClassOf(x,z) ^ subClassOf(y,z) -> shareKind(x,y)
    """
    rule_code = "IR36"

    LOGGER.debug(f"Starting rule {rule_code}.")

    query_string = """
    SELECT DISTINCT ?class_x ?class_y
    WHERE {
        ?class_z rdf:type gufo:Kind .
        ?class_x rdfs:subClassOf ?class_z .
        ?class_y rdfs:subClassOf ?class_z .
    } """

    query_result = ontology_graph.query(query_string)

    scior_share_kind = URIRef(SCIOR_NAMESPACE + "shareKind")

    for row in query_result:
        ontology_graph.add((row.class_x, scior_share_kind, row.class_y))

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir37(ontology_graph: Graph) -> None:
    """ Executes rule IR37 from group AUX.

    Code: IR37
    Definition: Kind(z) ^ subClassOf(x,z) ^ shareKind(x,y) -> subClassOf(y,z)
    """
    rule_code = "IR37"

    LOGGER.debug(f"Starting rule {rule_code}.")

    query_string = """
    PREFIX scior: <https://purl.org/scior/>
    SELECT DISTINCT ?class_y ?class_z
    WHERE {
        ?class_z rdf:type gufo:Kind .
        ?class_x rdfs:subClassOf ?class_z .
        ?class_x scior:shareKind ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_graph.add((row.class_y, RDFS.subClassOf, row.class_z))

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_aux(ontology_graph: Graph) -> None:
    """Executes all rules of the AUX group."""

    LOGGER.debug("Starting execution of all rules from group AUX.")

    ontology_graph.bind("scior", SCIOR_NAMESPACE)

    run_ir36(ontology_graph)
    run_ir37(ontology_graph)

    LOGGER.debug("Execution of all rules from group AUX completed.")
