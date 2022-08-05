""" Functions that allows human intervention and visualization for testing purposes. """
from os import path, remove

from rdflib import RDF, OWL

if __name__ != '__main':

    import logging

    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


    def print_list_file(var):
        """ Print a list to the test file /trash/delete.txt """

        test_file = "./trash/delete.txt"

        try:
            file_exists = path.exists(test_file)
            if file_exists:
                remove(test_file)
                logging.debug("Previously existent trash/delete.txt successfully deleted.")
            with open(test_file, 'a', encoding='utf-8') as f:
                for i in range(len(var)):
                    f.write(var[i] + "\n")
            logging.debug("New trash/delete.txt successfully created and printed.")
        except OSError:
            logging.error("Could not print in trash/delete.txt. Exiting program.")
            exit(1)


    def insert_triple(ontology):
        """ Allows user to manually insert a triple into the ontology for verifying its effects """

        input1 = input("Enter the Ontology entity:")
        input2 = input("Enter the relation number (1 for owl:subClassOf, 2 for rdf:type):")
        input3 = input("Enter the Ontology entity:")

        if input2 == "1":
            ontology.add((input1, OWL.subClassOf, input3))
        else:
            ontology.add((input1, RDF.type, input3))

        return ontology
