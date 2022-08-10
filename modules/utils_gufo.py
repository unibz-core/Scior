""" Functions associated with GUFOClass """


def get_from_gufo_lists(element, list_gufo_classes):
    """ Return lists of elements from GUFO is_list and not_list when gufo.uri matches element. """

    is_list = []
    not_list = []

    for i in range(len(list_gufo_classes)):
        if list_gufo_classes[i].uri == element:
            is_list = list_gufo_classes[i].is_list.copy()
            not_list = list_gufo_classes[i].not_list.copy()
            break

    return is_list, not_list





# TODO (@pedropaulofb): Crete function to verify if a class in an ontology is an instance of a GUFO class
# TODO (@pedropaulofb): Crete function to verify if a class in an ontology is a subclass of a GUFO class