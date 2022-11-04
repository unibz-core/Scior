""" Functions related to reading and writing OWL files using RDFLib. """

from rdflib import URIRef, RDF, RDFS, OWL

from modules.utils_rdf import get_ontology_uri


def save_ontology_gufo_statements(dataclass_list, ontology_graph):
    """ Receives the list of dataclasses and use its information for creating new statements in the ontology graph.
    Returns an updated ontology graph.
    """
    ontology_graph.bind("gufo", "http://purl.org/nemo/gufo#")

    for dataclass in dataclass_list:
        # Hierarchy of Types
        for is_type in dataclass.is_type:
            treated_name = treat_name(is_type)
            new_type = URIRef(treated_name)
            class_name = URIRef(dataclass.uri)
            ontology_graph.add((class_name, RDF.type, new_type))

        # Hierarchy of Individuals
        for is_individual in dataclass.is_individual:
            treated_name = treat_name(is_individual)
            new_individual = URIRef(treated_name)
            class_name = URIRef(dataclass.uri)
            ontology_graph.add((class_name, RDFS.subClassOf, new_individual))

    return ontology_graph


def save_ontology_file(end_date_time, ontology_graph, configurations):
    """
    Saves the ontology graph into a TTL file.
    If import_gufo parameter is set as True, the saved output is going to import the GUFO ontology.
    """

    if configurations["import_gufo"]:
        ontology_uri = get_ontology_uri(ontology_graph)
        gufo_import = URIRef("https://purl.org/nemo/gufo#")
        ontology_graph.add((ontology_uri, OWL.imports, gufo_import))

    # Creating report file
    output_file_name = configurations["ontology_path"][:-4] + "-" + end_date_time + ".out.ttl"
    ontology_graph.serialize(destination=output_file_name)


def treat_name(gufo_short_name):
    """
    Receives a short GUFO URI string (e.g., gufo:Kind) and
    returns a full GUFO URI string (e.g., http://purl.org/nemo/gufo#Kind).
    """

    gufo_url = "http://purl.org/nemo/gufo#"
    return gufo_url + gufo_short_name[5:]
