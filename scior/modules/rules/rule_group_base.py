""" Implementation of rules of group BASE. """

from rdflib import RDF, OWL, RDFS

from scior.modules.logger_config import initialize_logger

logger = initialize_logger()


def run_r01ag(ontology_graph):
    """ Executes rule R01Ag from group base.

    Code: R01Ag
    Definition: subClassOf(x,x)
    Description: rdfs:subClassOf is reflexive. All owl:Classe instances are rdfs:subClassOf themselves.
    """

    rule_code = "R01Ag"

    logger.debug(f"Starting rule {rule_code}")

    for ontology_class in ontology_graph.subjects(RDF.type, OWL.Class):
        ontology_graph.add((ontology_class, RDFS.subClassOf, ontology_class))

    logger.debug(f"Rule {rule_code} concluded")


def run_r02ag(ontology_graph):
    """ Executes rule R02Ag from group base.

    Code: R02Ag
    Definition: subClassOf(x,y) ^ subClassOf(y,z) -> subClassOf(x,z)
    Description: rdfs:subClassOf is transitive. All owl:Classe instances are rdfs:subClassOf of all their superclasses.
    """
    rule_code = "R02Ag"

    logger.debug(f"Starting rule {rule_code}")

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

    logger.debug(f"Rule {rule_code} concluded")


def execute_base_rules(ontology_graph):
    """Executes once all rules of the BASE group."""

    # Executing R02Ag first than R01Ag because it is faster and the results are the same.
    run_r02ag(ontology_graph)
    run_r01ag(ontology_graph)

    # TODO (@pedropaulofb): remove code line
    # safe_save_ontology_file(ontology_graph, "C:\\Users\\PFavatoBarcelos\\Dev\\Work\\Scior\\ontologies\\deletepp.ttl")
