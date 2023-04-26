""" Implementation of all rules from the group CWA. """
from rdflib import Graph, RDFS, URIRef
from rdflib.plugins.sparql.processor import SPARQLResult

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classification_to_not_type
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry
from scior.modules.resources_gufo import SCIOR_NAMESPACE
from scior.modules.rules.rule_group_ufo_some import treat_result_ufo_some
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def run_ir47(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule IR47 from group CWA.

    Code: IR47
    Definition: ~(E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^
                AntiRigidType(x) ^ Sortal(x) ^ subClassOf(x,y) -> ~Category(y)
    Description: Contraposition (~Q -> ~P) of rule IR30 (P -> Q).
    """

    rule_code = "IR47"

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


def run_ir48(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule IR48 from group CWA.

    Code: IR48
    Definition: ~(E y, z (subClassOf(y,x) ^ AntiRigidType(y) ^ subClassOf(z,x) ^ RigidType(z))) -> ~Mixin(x)
    Description: Contraposition (~Q -> ~P) of rule R25 (P -> Q).

    Added that the subclass cannot be the class itself.
    """

    rule_code = "IR48"

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


def run_ir49(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule IR49 from group CWA.

    Code: IR49
    Definition: ~(E y,z (y != z ^ Sortal(y) ^ Sortal(z) ^ ~shareKind(y,z) ^ (subClassOf(y,x) v shareSuperClass(x,y))) ^
                (subClassOf(z,x) v shareSuperClass(x,z))) -> ~NonSortal(x)
    Description: Contraposition (~Q -> ~P) of rule IR31 (P -> Q).
    """

    rule_code = "IR49"

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

    # Trating populated dictionary
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
                    # print(f"related {base_list_element} and {comp_list_element}")
                    class_x_dict[evaluated_class].remove(comp_list_element)

        # If the final list is smaller than two, than it cannot be a NonSortal:
        if len(class_x_dict[evaluated_class]) < 2:
            dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "NonSortal")

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir50(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule IR50 from group CWA.

    Code: IR50
    Definition: ~(E z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^ Role(x) ^ subClassOf(x,y) -> ~PhaseMixin(y)
    Description: Contraposition (~Q -> ~P) of rule IR43 (P -> Q). Variation A.
    """

    rule_code = "IR50"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:Role .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        }
        """

    query_result = ontology_graph.query(query_string)

    # Setting Y as not PhaseMixin if Z is known to not be (i.e., has in its not_type list) a Phase.
    for row in query_result:

        class_y = row.class_y.toPython()
        class_z = row.class_z.toPython()

        dataclass_y = get_dataclass_by_uri(ontology_dataclass_list, class_y)
        dataclass_z = get_dataclass_by_uri(ontology_dataclass_list, class_z)

        if "Phase" in dataclass_z.not_type:
            move_classification_to_not_type(ontology_dataclass_list, dataclass_y, "PhaseMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir51(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Implements rule IR50 from group CWA.

    Code: IR51
    Definition: ~(E z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))) ^ PhaseMixin(y) ^ subClassOf(x,y) -> ~Role(x)
    Description: Contraposition (~Q -> ~P) of rule IR43 (P -> Q). Variation B.
    """

    rule_code = "IR51"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_y ?class_z
        WHERE {
            ?class_y rdf:type gufo:PhaseMixin .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        }
        """

    query_result = ontology_graph.query(query_string)

    # Setting X as not Role if Z is known to not be (i.e., has in its not_type list) a Phase.
    for row in query_result:

        class_x = row.class_x.toPython()
        class_z = row.class_z.toPython()

        dataclass_x = get_dataclass_by_uri(ontology_dataclass_list, class_x)
        dataclass_z = get_dataclass_by_uri(ontology_dataclass_list, class_z)

        if "Phase" in dataclass_z.not_type:
            move_classification_to_not_type(ontology_dataclass_list, dataclass_x, "Role", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded.")

def execute_rules_ufo_cwa(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """Call execution all rules from the group UFO CWA."""

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_ir47(ontology_dataclass_list, ontology_graph)
    run_ir48(ontology_dataclass_list, ontology_graph)
    run_ir49(ontology_dataclass_list, ontology_graph)
    run_ir50(ontology_dataclass_list, ontology_graph)
    run_ir51(ontology_dataclass_list, ontology_graph)

    # for a, get list of not sc a,b and not sc b,a
    # remove all that do not shareKind
    # if in all elements from the remainding list Phase is in not_type,
    # then X is not a Phase


    # run_ir52(ontology_dataclass_list, ontology_graph)
    # run_ir53(ontology_dataclass_list, ontology_graph)
    # run_ir54(ontology_dataclass_list, ontology_graph)
    # run_ir55(ontology_dataclass_list, ontology_graph)
    # run_ir56(ontology_dataclass_list, ontology_graph)
    # run_ir57(ontology_dataclass_list, ontology_graph)
    # run_ir58(ontology_dataclass_list, ontology_graph)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
