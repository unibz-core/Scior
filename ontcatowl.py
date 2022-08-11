"""Main module for OntCatOWL"""

if __name__ == "__main__":

    from modules.utils_graph import get_list_root_classes, get_list_leaf_classes, get_superclasses, get_subclasses
    from modules.data_initialization_gufo import get_list_of_gufo_types, get_list_of_gufo_individuals
    from modules.data_initialization_ontology import initialize_ontology
    import logging
    from rdflib import Graph

    # TODO (@pedropaulofb): Set base level for printing log
    #   e.g., only print if called with -d parameter (debug)
    #   e.g., print debut only to file
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

    ontology = Graph()

    # TODO (@pedropaulofb): Read from argument
    # Input ontology to be evaluated
    try:
        ontology.parse("resources/d3fend.ttl")
    except OSError:
        logging.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    logging.debug("Initializing list of Ontology concepts.")
    ontology_classes = initialize_ontology(ontology)

    # TODO (@pedropaulofb): The ontology may already contain relations with GUFO. Treat that.

    # logging.debug("Initializing RDFS reasoning. This may take a while...")
    # st = time.time()
    # DeductiveClosure(RDFS_Semantics).expand(ontology)  # Performs RDFS inferences
    # et = time.time()
    # elapsed_time = round((et - st), 2)
    # logging.debug(f"Reasoning process completed in {elapsed_time} seconds.")

    logging.debug("Initializing list of GUFO concepts.")
    gufo_types = get_list_of_gufo_types()
    gufo_individuals = get_list_of_gufo_individuals()

    list_root = get_list_root_classes(ontology)
    list_leaf = get_list_leaf_classes(ontology)

    list_superclasses = get_superclasses(ontology, "http://d3fend.mitre.org/ontologies/d3fend.owl#AccessControlList")
    list_subclasses = get_subclasses(ontology, "http://d3fend.mitre.org/ontologies/d3fend.owl#AccessControlList")

    print(f"list_superclasses = \n{list_superclasses}\n")
    print(f"list_subclasses = \n{list_subclasses}\n")

    # From now on, the working entities are:  #   ontology: complete graph with inferences  #   ontology_classes: list of OntologyClasses to be manipulated  #   gufo_types: list of gufo types for reference  #   gufo_individuals: list of gufo individuals for reference

# TODO (@pedropaulofb): Create log file parallel to logs printed on std.out
#       (e.g., https://github.com/borntyping/jsonlog)
# TODO (@pedropaulofb): Use different colors for logs levels printed on std.out
#       (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
