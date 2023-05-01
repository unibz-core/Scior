""" Implementation of all rules from the group CWA. """
from rdflib import Graph, RDFS, URIRef

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classification_to_not_type, \
    move_classification_to_is_type
from scior.modules.resources_gufo import SCIOR_NAMESPACE
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def run_RC01(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC01 from group CWA.

        Definition: ~(E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^ AntiRigidType(x) ^
                    Sortal(x) ^ subClassOf(x,y) -> ~Category(y)
        Description: Contraposition (~Q -> ~P) of rule RS01 (P -> Q).
    """

    rule_code = "RC01"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:AntiRigidType , gufo:Sortal .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        }
        """

    query_result = ontology_graph.query(query_string)

    # Setting Y as not Category if Z is known to not be (i.e., has in its not_type list) a Rigid Sortal.
    for row in query_result:

        class_y = row.class_y.toPython()
        class_z = row.class_z.toPython()

        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
        dataclass_z = get_dataclass_by_uri(ontology_dataclass_list, class_z)

        if "RigidType" in dataclass_z.not_type and "Sortal" in dataclass_z.not_type:
            move_classification_to_not_type(ontology_dataclass_list, dataclass_y, "Category", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC02(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC02 from group CWA.

        Definition: ~(E y, z (subClassOf(y,x) ^ AntiRigidType(y) ^ subClassOf(z,x) ^ RigidType(z))) -> ~Mixin(x)
        Description: Contraposition (~Q -> ~P) of rule R25 (P -> Q).

        Added that the subclass cannot be the class itself.
    """

    rule_code = "RC02"

    LOGGER.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:
        list_subclasses = []
        is_or_can_rigid_subclass = 0
        is_or_can_antirigid_subclass = 0

        # Creating list of subclasses for a dataclass
        for subclass in ontology_graph.subjects(RDFS.subClassOf, URIRef(ontology_dataclass.uri)):
            list_subclasses.append(subclass.toPython())

        # Removing the class itself from its list of subclasses
        list_subclasses.remove(ontology_dataclass.uri)
        num_subclasses = len(list_subclasses)

        for subclass in list_subclasses:
            subclass_dataclass = get_dataclass_by_uri(ontology_dataclass_list, subclass)

            # At least one subclass must not have RigidType in its not_type list
            if "RigidType" not in subclass_dataclass.not_type:
                is_or_can_rigid_subclass += 1

            # At least one subclass must not have AntiRigidType in its not_type list
            if "AntiRigidType" not in subclass_dataclass.not_type:
                is_or_can_antirigid_subclass += 1

        # If the number of subclasses is less than two it cannot be a Mixin
        if num_subclasses < 2 or is_or_can_rigid_subclass == 0 or is_or_can_antirigid_subclass == 0:
            move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC03(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC03 from group CWA.

        Definition: ~(E y,z (x != y ^ x != z ^ subClassOf(x,y) ^ subClassOf(z,y)) -> Kind(x)
        Description: A class without supertypes or subtypes is a Kind.
    """

    rule_code = "RC03"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x
        WHERE {
            ?class_x rdf:type owl:Class .
            FILTER NOT EXISTS {
                ?class_y rdf:type owl:Class .
                ?class_y rdfs:subClassOf ?class_x .
                FILTER (?class_y != ?class_x)
            }
            FILTER NOT EXISTS {
                ?class_z rdf:type owl:Class .
                ?class_x rdfs:subClassOf ?class_z .
                FILTER (?class_z != ?class_x)
            }
        }
        """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_x.toPython())
        move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC04(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC04 from group CWA.

        Definition: ~(E y (subClassOf (x,y) ^ Kind(y))) -> ~Sortal(x)
        Description: Contraposition (~Q -> ~P) of rule R35 (P -> Q).
                    If a class does not have a superclass that can be a Kind then it is not a Sortal.
    """

    rule_code = "RC04"

    LOGGER.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:

        # Creating list of superclasses that can be a Kind
        for superclass in ontology_graph.objects(URIRef(ontology_dataclass.uri), RDFS.subClassOf):

            # Else, check:
            superclass_dataclass = get_dataclass_by_uri(ontology_dataclass_list, superclass.toPython())

            # Checking if there is at least one superclass that IS or CAN BE a Kind. If there is, continue to the next

            if "Kind" not in superclass_dataclass.not_type:
                break

        # If a break is not found:
        # It means that all supertypes cannot be a Kind and that the evaluated dataclass cannot be a Sortal
        else:
            move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC05(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC05 from group CWA.

        Definition: ~(E y,z (y!=z ^ Sortal(y) ^ Sortal(z) ^ ~shareKind(y,z) ^ (subClassOf(y,x) v shareSuperClass(x,y)))^
                    (subClassOf(z,x) v shareSuperClass(x,z))) -> ~NonSortal(x)
        Description: Contraposition (~Q -> ~P) of rule RS02 (P -> Q).
    """

    rule_code = "RC05"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        PREFIX scior: <https://purl.org/scior/>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_y rdfs:subClassOf|scior:shareSuperClass ?class_x .
        }
        """

    query_result = ontology_graph.query(query_string)

    scior_share_kind = URIRef(SCIOR_NAMESPACE + "shareKind")
    class_x_dict = {}

    # Creating dictionary for all evaluated classes with all classes related via subclasses or shareSuperClass
    for row in query_result:

        class_x = row.class_x.toPython()
        class_y = row.class_y.toPython()

        # Removing itself from the list
        if class_x == class_y:
            continue

        # Removing class_y if it cannot be a Sortal
        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
        if "Sortal" in dataclass_y.not_type:
            continue

        # If dictionary entry does not exist, create a new one
        if class_x not in class_x_dict.keys():
            class_x_dict[class_x] = []

        # Populate dictionary
        class_x_dict[class_x].append(class_y)

    # Treating populated dictionary
    for evaluated_class in class_x_dict.keys():

        # If the number of elements is smaller than two, set as not NonSortal
        if len(class_x_dict[evaluated_class]) < 2:
            dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "NonSortal")
            continue

        # Removing from evaluated_class's all elements that shareKind (leaving just one for each Kind)
        for base_list_element in class_x_dict[evaluated_class]:
            for comp_list_element in class_x_dict[evaluated_class]:
                if base_list_element == comp_list_element:
                    continue
                elif (URIRef(base_list_element), scior_share_kind, URIRef(comp_list_element)) in ontology_graph:
                    class_x_dict[evaluated_class].remove(comp_list_element)

        # If the final list is smaller than two, than it cannot be a NonSortal:
        if len(class_x_dict[evaluated_class]) < 2:
            dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "NonSortal")

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC06(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC06 from group CWA.

        Definition: ~(E z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^ Role(x) ^ subClassOf(x,y) -> ~PhaseMixin(y)
        Description: Contraposition (~Q -> ~P) of rule RS06 (P -> Q). Variation A.
    """

    rule_code = "RC06"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:Role .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
            FILTER(?class_x != ?class_z)
            FILTER(?class_y != ?class_z)
            FILTER(?class_x != ?class_y)
        }
        """

    query_result = ontology_graph.query(query_string)

    # Setting Y as not PhaseMixin if Z is known to not be (i.e., has in its not_type list) a Phase.
    for row in query_result:

        class_y = row.class_y.toPython()
        class_z = row.class_z.toPython()

        if class_y == class_z:
            continue

        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
        dataclass_z = get_dataclass_by_uri(ontology_dataclass_list, class_z)

        if "Phase" in dataclass_z.not_type:
            move_classification_to_not_type(ontology_dataclass_list, dataclass_y, "PhaseMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC07(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC07 from group CWA.

        Definition: ~(E z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^ PhaseMixin(y) ^ subClassOf(x,y) -> ~Role(x)
        Description: Contraposition (~Q -> ~P) of rule RS06 (P -> Q). Variation B.
    """

    rule_code = "RC07"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_z
        WHERE {
            ?class_y rdf:type gufo:PhaseMixin .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
            FILTER(?class_x != ?class_z)
            FILTER(?class_y != ?class_z)
            FILTER(?class_x != ?class_y)
        }
        """

    query_result = ontology_graph.query(query_string)

    # Setting X as not Role if Z is known to not be (i.e., has in its not_type list) a Phase.
    for row in query_result:

        class_x = row.class_x.toPython()
        class_z = row.class_z.toPython()

        if class_x == class_z:
            continue

        dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, class_x)
        dataclass_z = get_dataclass_by_uri(ontology_dataclass_list, class_z)

        if "Phase" in dataclass_z.not_type:
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "Role", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC08(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC08 from group CWA.

        Definition: ~(E y (Phase (y) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x))) -> ~Phase(x)
        Description: Contraposition (~Q -> ~P) of rule RS07 (P -> Q).
                    A class with a single phase cannot be a Kind.
    """

    rule_code = "RC08"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX scior: <https://purl.org/scior/>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x scior:shareKind ?class_y .
        }
        """

    query_result = ontology_graph.query(query_string)

    # Creating dictionary for query results
    class_x_dict = {}
    for row in query_result:

        class_x = row.class_x.toPython()
        class_y = row.class_y.toPython()

        # A dictionary key is going to be created for each Phase candidate only
        dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, class_x)
        if "Phase" in dataclass_x.not_type:
            continue

        # If a new dictionary entry does not exist, create a new one
        if class_x not in class_x_dict.keys():
            class_x_dict[class_x] = []

        # Removing itself from the list
        if class_x == class_y:
            continue

        # Excluding population of class_y if it cannot be a Phase
        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
        if "Phase" in dataclass_y.not_type:
            continue

        # Excluding population of class_y if it is a subclass of class_x
        if (URIRef(dataclass_y.uri), RDFS.subClassOf, URIRef(dataclass_x.uri)) in ontology_graph:
            continue

        # Populate dictionary
        class_x_dict[class_x].append(class_y)

    for evaluated_class in class_x_dict.keys():
        if len(class_x_dict[evaluated_class]) == 0:
            dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "Phase", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC09(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC09 from group CWA.

        Definition: ~(E y (Category (y) ^ isSubClassOf(x,y))) -> ~PhaseMixin(x)
        Description: Contraposition (~Q -> ~P) of rule R45 (P -> Q).
                If a class does not have a superclass that can be a Category then it is not a PhaseMixin.
    """

    rule_code = "RC09"

    LOGGER.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:

        # Creating list of superclasses that can be a Category
        for superclass in ontology_graph.objects(URIRef(ontology_dataclass.uri), RDFS.subClassOf):

            # Else, check:
            superclass_dataclass = get_dataclass_by_uri(ontology_dataclass_list, superclass.toPython())

            # Checking if is at least one superclass that IS or CAN BE a Category. If there is, continue to the next.

            if "Category" not in superclass_dataclass.not_type:
                break

        # If a break is not found:
        # It means that all supertypes cannot be a Category and that the evaluated dataclass cannot be a PhaseMixin
        else:
            move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC10(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC10 from group CWA.

        Definition: ~(E z (PhaseMixin(z) ^ Category(y) ^ subClassOf(x,y) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^
                    isSubClassOf(z,y))) -> ~PhaseMixin(x)
        Description: Contraposition (~Q -> ~P) of rule RS09 (P -> Q). Variation A.
                    A class X with a known sibling PhaseMixin Z (Z!=X) can only be a PhaseMixin if it has at least one
                    common superclass X that can be a Category.
    """

    rule_code = "RC10"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdfs:subClassOf ?class_y .
            ?class_z rdfs:subClassOf ?class_y .

            ?class_z rdf:type gufo:PhaseMixin .

            MINUS {?class_x rdfs:subClassOf ?class_z}
            MINUS {?class_z rdfs:subClassOf ?class_x}
        }
        """

    query_result = ontology_graph.query(query_string)

    dictionary_y = {}

    for row in query_result:

        class_y = row.class_y.toPython()
        class_x = row.class_x.toPython()

        # If dictionary entry does not exist, create a new one
        if class_y not in dictionary_y.keys():
            dictionary_y[class_y] = []

        dictionary_y[class_y].append(class_x)

    for class_y in dictionary_y.keys():
        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)

        # If the superclass Y cannot be a Category, then all its subtypes (different then Z) cannot be PhaseMixins
        if "Category" in dataclass_y.not_type:
            for class_x in dictionary_y[class_y]:
                dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, class_x)
                move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "PhaseMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_RC11(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule RC11 from group CWA.

        Definition: ~(E z (PhaseMixin(z) ^ PhaseMixin(x) ^ subClassOf(x,y) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^
                    isSubClassOf(z,y))) -> ~Category(y)
        Description: Contraposition (~Q -> ~P) of rule RS09 (P -> Q). Variation B.
                    A class Y with a known PhaseMixin Z subclass can only be a Category if it at least a
                    subclass X (Y!=Z) that can be a PhaseMixin.
    """

    rule_code = "RC11"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdfs:subClassOf ?class_y .
            ?class_z rdfs:subClassOf ?class_y .

            ?class_z rdf:type gufo:PhaseMixin .

            MINUS {?class_x rdfs:subClassOf ?class_z}
            MINUS {?class_z rdfs:subClassOf ?class_x}
        }
        """

    query_result = ontology_graph.query(query_string)

    dictionary_y = {}

    for row in query_result:

        class_y = row.class_y.toPython()
        class_x = row.class_x.toPython()

        # If dictionary entry does not exist, create a new one
        if class_y not in dictionary_y.keys():
            dictionary_y[class_y] = []

        dictionary_y[class_y].append(class_x)

    for class_y in dictionary_y.keys():
        for class_x in dictionary_y[class_y]:
            dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, class_x)

            # If positive, at least one subclass can be a PhaseMixin, then Y can be a Category.
            if "PhaseMixin" not in dataclass_x.not_type:
                break
        else:
            # If it is here is because all elements in the list dictionary_y[class_y] cannot be PhaseMixins
            dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
            move_classification_to_not_type(ontology_dataclass_list, dataclass_y, "Category", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_cwa(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Call execution all rules from the group UFO CWA. """

    LOGGER.debug("Starting execution of all rules from group UFO CWA.")

    run_RC01(ontology_dataclass_list, ontology_graph)
    run_RC02(ontology_dataclass_list, ontology_graph)
    run_RC03(ontology_dataclass_list, ontology_graph)
    run_RC04(ontology_dataclass_list, ontology_graph)
    run_RC05(ontology_dataclass_list, ontology_graph)
    run_RC06(ontology_dataclass_list, ontology_graph)
    run_RC07(ontology_dataclass_list, ontology_graph)
    run_RC08(ontology_dataclass_list, ontology_graph)
    run_RC09(ontology_dataclass_list, ontology_graph)
    run_RC10(ontology_dataclass_list, ontology_graph)
    run_RC11(ontology_dataclass_list, ontology_graph)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
