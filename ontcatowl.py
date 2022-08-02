"""Main module for OntCatOWL"""

if __name__ == "__main__":

    import logging

    from rdflib import Graph

    from modules.ontcatowl_dataclasses import initialize_gufo_list

    # TODO (@pedropaulofb): Set base level for printing log
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

    gufo = Graph()
    ontology = Graph()

    # Input GUFO ontology
    # TODO (@pedropaulofb): Change for the complete version of GUFO after the tests are finished.
    try:
        gufo.parse("resources/gufoEndurantsOnly.ttl")
    except OSError:
        logging.error("Could not load resources/gufoEndurantsOnly.ttl file. Exiting program.")
        exit(1)

    # TODO (@pedropaulofb): Read from argument
    # Input ontology to be evaluated
    try:
        ontology.parse("resources/d3fend.ttl")
    except OSError:
        logging.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    # TODO (@pedropaulofb): Read all classes from input ontology and create a list with no repetitions

    logging.debug("Initializing RDFS inferences. This may take a while...")
    # DeductiveClosure(RDFS_Semantics).expand(ontology)  # Performs RDFS inferences

    logging.debug("Initializing list of GUFO concepts.")
    gufo_list = []
    initialize_gufo_list(gufo_list)

    # TODO (@pedropaulofb): Create log file parallel to logs printed on std.out  #  (e.g., https://github.com/borntyping/jsonlog)  # TODO (@pedropaulofb): Use different colors for logs levels printed on std.ou  #  (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)  # TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions  # TODO (@pedropaulofb): Evaluate on Linux before release first version  # TODO (@pedropaulofb): update requirements.txt
