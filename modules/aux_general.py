""" General auxiliary functions. """

if __name__ != "__main__":

    def has_duplicates(list):
        """ Check if given list contains any duplicated element """
        if len(list) == len(set(list)):
            return False
        else:
            return True
