""" Class to store and calculate all information about results' information for the Scior execution.  """


class ResultsInformationClass(object):
    """ Class to store all statistics and results information for the Scior execution. """

    def __init__(self):
        # CLASSES LISTS

        self.tu_list_b:list[str] = []
        self.pk_list_b:list[str] = []
        self.tk_list_b:list[str] = []

        self.tu_list_a:list[str] = []
        self.pk_list_a:list[str] = []
        self.tk_list_a:list[str] = []

        # NUMBERS FOR CLASSIFICATIONS

        # Situation

        self.num_uc_b: int = -1
        self.num_kc_b: int = -1

        self.num_uc_a: int = -1
        self.num_kc_a: int = -1

    def calculate_information(self):
        """ Calculate information (derived data results) with the numbers stored in the class's attributes.
            Zero division error does not need to be treated, as the number of classes is never zero.
        """

        # NUMBERS FOR CLASSES

        # Situation

        self.num_tu_b: int = len(self.tu_list_b)
        self.num_pk_b: int = len(self.pk_list_b)
        self.num_tk_b: int = len(self.tk_list_b)

        self.num_tu_a: int = len(self.tu_list_a)
        self.num_pk_a: int = len(self.pk_list_a)
        self.num_tk_a: int = len(self.tk_list_a)

        # Totals

        self.num_classes_b: int = self.num_tu_b + self.num_pk_b + self.num_tk_b
        self.num_classes_a: int = self.num_tu_a + self.num_pk_a + self.num_tk_a

        # TODO (@pedropaulofb): Implement
        # Validate totals for classes
        # if self.num_classif_b != self.num_classif_a:
        #     LOGGER.error("")

        # Difference

        self.num_tu_d: int = self.num_tu_a - self.num_tu_b
        self.num_pk_d: int = self.num_pk_a - self.num_pk_b
        self.num_tk_d: int = self.num_tk_a - self.num_tk_b

        # NUMBERS FOR CLASSIFICATIONS

        # Totals

        self.num_classif_b: int = self.num_uc_b + self.num_kc_b
        self.num_classif_a: int = self.num_uc_a + self.num_kc_a

        # TODO (@pedropaulofb): Implement
        # Validate totals for classifications
        # if self.num_classif_b != self.num_classif_a:
        #     LOGGER.error("")

        # Difference

        self.num_uc_d: int = self.num_uc_a - self.num_uc_b
        self.num_kc_d: int = self.num_kc_a - self.num_kc_b

        # PERCENTAGES FOR CLASSES

        # Situation (before/total and after/total for each type)

        self.per_tu_b: float = self.num_tu_b / self.num_classes_b
        self.per_pk_b: float = self.num_pk_b / self.num_classes_b
        self.per_tk_b: float = self.num_tk_b / self.num_classes_b

        self.per_tu_a: float = self.num_tu_a / self.num_classes_a
        self.per_pk_a: float = self.num_pk_a / self.num_classes_a
        self.per_tk_a: float = self.num_tk_a / self.num_classes_a

        # Difference (after - before)

        self.per_tu_d: float = self.per_tu_a - self.per_tu_b
        self.per_pk_d: float = self.per_pk_a - self.per_pk_b
        self.per_tk_d: float = self.per_tk_a - self.per_tk_b

        # PERCENTAGES FOR CLASSIFICATIONS

        # Situation (before/total and after/total)

        self.per_uc_b: float = self.num_uc_b / self.num_classif_b
        self.per_kc_b: float = self.num_kc_b / self.num_classif_b

        self.per_uc_a: float = self.num_uc_a / self.num_classif_a
        self.per_kc_a: float = self.num_kc_a / self.num_classif_a

        # Difference (after - before)

        self.per_uc_d: float = self.per_uc_a - self.per_uc_b
        self.per_kc_d: float = self.per_kc_a - self.per_kc_b
