if __name__ != "__main__":

    import logging
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

    def duplicated_same_list():
        duplicated_list = ""
        duplicated_found = False

        # same for is_type - duplicated_list = "is_type"
        # same for is_individual - duplicated_list = "is_individual"
        # same for can_type - duplicated_list = "can_type"
        # same for can_individual - duplicated_list = "can_individual"
        # same for not_type - duplicated_list = "not_type"
        # same for not_individual - duplicated_list = "not_individual"

        if duplicated_found:
            logging.error(
                f"INCONSISTENCY DETECTED: Same element in two lists for element {self.name} in list {duplicated_list}")
            exit(1)


    def correct_number_of_elements(self):  # Sum of elements from all lists must be equal to X
        logging.error("")
        exit(1)


    def duplicated_other_list(self):  # No same string must be in two lists at the same time.
        logging.error("")
        exit(1)
