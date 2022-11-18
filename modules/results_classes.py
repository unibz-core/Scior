""" Classes used as data structures for stats data. 

tu = totally unknown
pk = partially known
tk = totally known

stats = statistics
classif = classifications
indiv = individuals

_v = value
_p = percentage
_d = difference

_b = before
_a = after

"""

from modules.logger_config import initialize_logger


class dataclass_stats(object):
    """ Class that contains the statistics for a single dataclass. """

    def __init__(self, ontology_dataclass):
        self.uri = ontology_dataclass.uri

        self.unknown_types = len(ontology_dataclass.can_type)
        self.unknown_individuals = len(ontology_dataclass.can_individual)

        self.known_types = len(ontology_dataclass.is_type) + len(ontology_dataclass.not_type)
        self.known_individuals = len(ontology_dataclass.is_individual) + len(ontology_dataclass.not_individual)


class list_classes_by_situation(object):
    """ Class that contains the uri of all classes in a specific situation.

    Situation field admitted values: "Totally Unknown", "Partially Known", "Totally Known".
    """

    def __init__(self, situation, list_uris_types, list_uris_individuals, list_uris_all):

        logger = initialize_logger()
        if situation == "Totally Unknown" or situation == "Partially Known" or situation == "Totally Known":
            self.situation = situation
            self.list_uris_types = list_uris_types
            self.list_uris_individuals = list_uris_individuals
            self.list_uris_all = list_uris_all
        else:
            logger.error("Unknown situation informed to list_classes_by_situation. Program aborted.")
            exit(1)


class classes_stats(object):
    """ Stores stats for all classes in a given time measurement (before, after, etc.). """

    def __init__(self):
        self.total_classes_number = -1

        # Values
        self.tu_classes_types_v = -1
        self.tu_classes_indiv_v = -1
        self.tu_classes_all_v = -1

        self.pk_classes_types_v = -1
        self.pk_classes_indiv_v = -1
        self.pk_classes_all_v = -1

        self.tk_classes_types_v = -1
        self.tk_classes_indiv_v = -1
        self.tk_classes_all_v = -1

    def calculate(self):
        # Percentages
        self.tu_classes_types_p = (self.tu_classes_types_v / self.total_classes_number) * 100
        self.tu_classes_indiv_p = (self.tu_classes_indiv_v / self.total_classes_number) * 100
        self.tu_classes_all_p = (self.pk_classes_all_v / self.total_classes_number) * 100

        self.pk_classes_types_p = (self.pk_classes_types_v / self.total_classes_number) * 100
        self.pk_classes_indiv_p = (self.pk_classes_indiv_v / self.total_classes_number) * 100
        self.pk_classes_all_p = (self.pk_classes_all_v / self.total_classes_number) * 100

        self.tk_classes_types_p = (self.tk_classes_types_v / self.total_classes_number) * 100
        self.tk_classes_indiv_p = (self.tk_classes_indiv_v / self.total_classes_number) * 100
        self.tk_classes_all_p = (self.tk_classes_all_v / self.total_classes_number) * 100

    def validate(self):
        # Consistency verifications for classes:
        total_classes_types = self.tu_classes_types_v + self.pk_classes_types_v + self.tk_classes_types_v
        total_classes_indiv = self.tu_classes_indiv_v + self.pk_classes_indiv_v + self.tk_classes_indiv_v
        total_classes_all = self.tu_classes_all_v + self.pk_classes_all_v + self.tk_classes_all_v

        if (total_classes_types + total_classes_indiv + total_classes_all) != (3 * self.total_classes_number):
            logger = initialize_logger()
            logger.error("Sum of number of classes is incorrect when calculating statistics. Program aborted.")
            exit(1)


class classifications_stats(object):
    """ Stores stats for all classes in a given time measurement (before, after, etc.). """

    def __init__(self):
        self.total_classif_number = -1

        # Values
        self.total_classif_types_v = -1
        self.total_classif_indiv_v = -1

        self.unknown_classif_types_v = -1
        self.unknown_classif_indiv_v = -1

        self.known_classif_types_v = -1
        self.known_classif_indiv_v = -1

    def calculate(self):
        self.unknown_classif_total_v = self.unknown_classif_types_v + self.unknown_classif_indiv_v
        self.known_classif_total_v = self.known_classif_types_v + self.known_classif_indiv_v

        # Percentages
        self.total_classif_types_p = (self.total_classif_types_v / self.total_classif_number) * 100
        self.total_classif_indiv_p = (self.total_classif_indiv_v / self.total_classif_number) * 100

        self.unknown_classif_types_p = (self.unknown_classif_types_v / self.total_classif_number) * 100
        self.known_classif_types_p = (self.known_classif_types_v / self.total_classif_number) * 100

        self.unknown_classif_indiv_p = (self.unknown_classif_indiv_v / self.total_classif_number) * 100
        self.known_classif_indiv_p = (self.known_classif_indiv_v / self.total_classif_number) * 100

        self.unknown_classif_total_p = (self.unknown_classif_total_v / self.total_classif_number) * 100
        self.known_classif_total_p = (self.known_classif_total_v / self.total_classif_number) * 100

    def validate(self):
        if self.unknown_classif_total_v + self.known_classif_total_v != self.total_classif_number:
            logger = initialize_logger()
            logger.error("Sum of number of classifications is incorrect when calculating statistics. Program aborted.")
            exit(1)


class comparission_stats(object):
    """ Stores 4 direct  data structures and attributes containing stats from the difference of these 4 lists.:
        - classes stats before. type: classes_stats
        - classifications stats before. type: classifications_stats
        - classes stats after. type: classes_stats
        - classifications stats after. type: classifications_stats
    """

    def __init__(self, classes_stats_b, classifications_stats_b, classes_stats_a,
                 classifications_stats_a):
        # CLASSES - asserted
        self.classes_stats_b = classes_stats_b
        self.classes_stats_a = classes_stats_a

        # CLASSIFICATIONS - asserted
        self.classif_stats_b = classifications_stats_b
        self.classif_stats_a = classifications_stats_a

    def calculate(self):
        # CLASSES - calculated values
        self.tu_classes_types_v_d = self.classes_stats_a.tu_classes_types_v - self.classes_stats_b.tu_classes_types_v
        self.tu_classes_indiv_v_d = self.classes_stats_a.tu_classes_indiv_v - self.classes_stats_b.tu_classes_indiv_v
        self.tu_classes_all_v_d = self.classes_stats_a.tu_classes_all_v - self.classes_stats_b.tu_classes_all_v

        self.pk_classes_types_v_d = self.classes_stats_a.pk_classes_types_v - self.classes_stats_b.pk_classes_types_v
        self.pk_classes_indiv_v_d = self.classes_stats_a.pk_classes_indiv_v - self.classes_stats_b.pk_classes_indiv_v
        self.pk_classes_all_v_d = self.classes_stats_a.pk_classes_all_v - self.classes_stats_b.pk_classes_all_v

        self.tk_classes_types_v_d = self.classes_stats_a.tk_classes_types_v - self.classes_stats_b.tk_classes_types_v
        self.tk_classes_indiv_v_d = self.classes_stats_a.tk_classes_indiv_v - self.classes_stats_b.tk_classes_indiv_v
        self.tk_classes_all_v_d = self.classes_stats_a.tk_classes_all_v - self.classes_stats_b.tk_classes_all_v

        # CLASSES - calculated percentages
        self.tu_classes_types_p_d = self.classes_stats_a.tu_classes_types_p - self.classes_stats_b.tu_classes_types_p
        self.tu_classes_indiv_p_d = self.classes_stats_a.tu_classes_indiv_p - self.classes_stats_b.tu_classes_indiv_p
        self.tu_classes_all_p_d = self.classes_stats_a.tu_classes_all_p - self.classes_stats_b.tu_classes_all_p

        self.pk_classes_types_p_d = self.classes_stats_a.pk_classes_types_p - self.classes_stats_b.pk_classes_types_p
        self.pk_classes_indiv_p_d = self.classes_stats_a.pk_classes_indiv_p - self.classes_stats_b.pk_classes_indiv_p
        self.pk_classes_all_p_d = self.classes_stats_a.pk_classes_all_p - self.classes_stats_b.pk_classes_all_p

        self.tk_classes_types_p_d = self.classes_stats_a.tk_classes_types_p - self.classes_stats_b.tk_classes_types_p
        self.tk_classes_indiv_p_d = self.classes_stats_a.tk_classes_indiv_p - self.classes_stats_b.tk_classes_indiv_p
        self.tk_classes_all_p_d = self.classes_stats_a.tk_classes_all_p - self.classes_stats_b.tk_classes_all_p

        # CLASSIFICATIONS - calculated values
        self.total_classif_types_v_d = self.classif_stats_a.total_classif_types_v - self.classif_stats_b.total_classif_types_v
        self.total_classif_indiv_v_d = self.classif_stats_a.total_classif_indiv_v - self.classif_stats_b.total_classif_indiv_v

        self.unknown_classif_types_v_d = self.classif_stats_a.unknown_classif_types_v - self.classif_stats_b.unknown_classif_types_v
        self.known_classif_types_v_d = self.classif_stats_a.known_classif_types_v - self.classif_stats_b.known_classif_types_v

        self.unknown_classif_indiv_v_d = self.classif_stats_a.unknown_classif_indiv_v - self.classif_stats_b.unknown_classif_indiv_v
        self.known_classif_indiv_v_d = self.classif_stats_a.known_classif_indiv_v - self.classif_stats_b.known_classif_indiv_v

        self.unknown_classif_total_v_d = self.classif_stats_a.unknown_classif_total_v - self.classif_stats_b.unknown_classif_total_v
        self.known_classif_total_v_d = self.classif_stats_a.known_classif_total_v - self.classif_stats_b.known_classif_total_v

        # CLASSIFICATIONS - calculated percentages
        self.total_classif_types_p_d = self.classif_stats_a.total_classif_types_p - self.classif_stats_b.total_classif_types_p
        self.total_classif_indiv_p_d = self.classif_stats_a.total_classif_indiv_p - self.classif_stats_b.total_classif_indiv_p

        self.unknown_classif_types_p_d = self.classif_stats_a.unknown_classif_types_p - self.classif_stats_b.unknown_classif_types_p
        self.known_classif_types_p_d = self.classif_stats_a.known_classif_types_p - self.classif_stats_b.known_classif_types_p

        self.unknown_classif_indiv_p_d = self.classif_stats_a.unknown_classif_indiv_p - self.classif_stats_b.unknown_classif_indiv_p
        self.known_classif_indiv_p_d = self.classif_stats_a.known_classif_indiv_p - self.classif_stats_b.known_classif_indiv_p

        self.unknown_classif_total_p_d = self.classif_stats_a.unknown_classif_total_p - self.classif_stats_b.unknown_classif_total_p
        self.known_classif_total_p_d = self.classif_stats_a.known_classif_total_p - self.classif_stats_b.known_classif_total_p
