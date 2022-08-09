""" Functions that allows human intervention and visualization for testing purposes. """
from os import path, remove

from rdflib import RDF, RDFS, URIRef

import logging

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


def erase_existing_file(file):
    """ If a file exists, remove it """

    file_exists = path.exists(file)

    if file_exists:
        remove(file)
        logging.debug(f"Previously existent {file} successfully deleted.")


def print_list_file(var):
    """ Print a list to the test file /trash/delete.txt """

    test_file = "./trash/delete.txt"

    try:
        erase_existing_file(test_file)
        with open(test_file, 'a', encoding='utf-8') as f:
            for i in range(len(var)):
                f.write(var[i] + "\n")
        logging.debug("New trash/delete.txt successfully created and printed.")
    except OSError:
        logging.error("Could not print in trash/delete.txt. Exiting program.")
        exit(1)


def safe_output_file(graph):
    """ Save a graph in a file """

    output_file = "./trash/ontology.ttl"

    try:
        erase_existing_file(output_file)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(graph.serialize(format="turtle"))
            logging.debug("New trash/ontology.ttl successfully created and written.")
    except OSError:
        logging.error(f"\nCould not WRITE file {output_file}. Exiting program.\n")
        exit(1)


def insert_triple(ontology):
    """ Allows user to manually insert a triple into the ontology for verifying its effects """

    input1 = input("Enter the Ontology entity: ")
    subject_uri = URIRef(input1)

    input2 = input("Enter the relation number (1 for rdfs:subClassOf, 2 for rdf:type): ")

    input3 = input("Enter the Ontology entity: ")
    object_uri = URIRef(input3)

    if input2 == "1":
        ontology.add((subject_uri, RDFS.subClassOf, object_uri))
        logging.debug(f"The following triple was inserted into the ontology: {input1} rdfs:subClassOf {input3}.")
    else:
        ontology.add((subject_uri, RDF.type, object_uri))
        logging.debug(f"The following triple was inserted into the ontology: {input1} rdf:type {input3}.")

    return ontology


def begin_test(ontology):
    """ Creates a test loop """

    cont = "y"

    while cont == "y" or cont == "Y":
        ontology = insert_triple(ontology)
        # TODO (@pedropaulofb): Insert processing here
        safe_output_file(ontology)
        cont = input("Continue (Y/N)?: ")
