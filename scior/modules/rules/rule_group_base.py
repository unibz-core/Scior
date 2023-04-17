""" Implementation of rules of group BASE. """

from rdflib import RDF, OWL, RDFS, URIRef

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()
SCIOR_NAMESPACE = "https://purl.org/scior/"


def run_r01ag(ontology_graph):
    """ Executes rule R01Ag from group base.

    Code: R01Ag
    Definition: subClassOf(x,x)
    Description: rdfs:subClassOf is reflexive. All owl:Classe instances are rdfs:subClassOf themselves.
    """

    rule_code = "R01Ag"

    LOGGER.debug(f"Starting rule {rule_code}")

    for ontology_class in ontology_graph.subjects(RDF.type, OWL.Class):
        ontology_graph.add((ontology_class, RDFS.subClassOf, ontology_class))

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r02ag(ontology_graph):
    """ Executes rule R02Ag from group base.

    Code: R02Ag
    Definition: subClassOf(x,y) ^ subClassOf(y,z) -> subClassOf(x,z)
    Description: rdfs:subClassOf is transitive. All owl:Classe instances are rdfs:subClassOf of all their superclasses.
    """
    rule_code = "R02Ag"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    SELECT DISTINCT ?subclass ?superclass
    WHERE {
        ?subclass rdf:type owl:Class .
        ?superclass rdf:type owl:Class .
        ?subclass rdfs:subClassOf+ ?superclass .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_graph.add((row.subclass, RDFS.subClassOf, row.superclass))

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r30ag(ontology_graph):
    """ Executes rule R30Ag from group BASE.

    Code: R30Ag
    Definition: subClassOf(x,z) ^ subClassOf(y,z) -> shareSuperClass(x,y)
    """
    rule_code = "R30Ag"

    LOGGER.debug(f"Starting rule {rule_code}.")

    query_string = """
    SELECT DISTINCT ?class_x ?class_y
    WHERE {
        ?class_x rdfs:subClassOf ?class_z .
        ?class_y rdfs:subClassOf ?class_z .
    } """

    query_result = ontology_graph.query(query_string)

    scior_share_super_class = URIRef(SCIOR_NAMESPACE + "shareSuperClass")

    for row in query_result:
        ontology_graph.add((row.class_x, scior_share_super_class, row.class_y))

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_base(ontology_graph):
    """Executes once all rules of the group BASE ."""

    LOGGER.debug("Starting execution of all rules from group BASE.")

    # Executing R02Ag first than R01Ag because it is faster and the results are the same.
    run_r02ag(ontology_graph)
    run_r01ag(ontology_graph)
    run_r30ag(ontology_graph)

    LOGGER.debug("Execution of all rules from group BASE completed.")
