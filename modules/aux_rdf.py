""" Auxiliary functions for extending and complementing RDFLib """

if __name__ != "__main__":

    def has_prefix(graph, prefix):
        """ Return boolean indicating if the argument prefix exists in the graph"""
        result = False

        for pre, nam in graph.namespaces():
            if prefix == pre:
                result = True

        return result


    def has_namespace(graph, namespace):
        """ Return boolean indicating if the argument namespace exists in the graph.
            The argument namespace must be provided without the surrounding <>"""
        result = False

        for pre, nam in graph.namespaces():
            if namespace == nam.n3()[1:-1]:
                result = True

        return result


    def list_prefixes(graph):
        """ Return a list of all prefixes in the graph"""
        result = []

        for pre, nam in graph.namespaces():
            result.append(pre)

        return result


    def list_namespaces(graph):
        """ Return a list of all namespaces in the graph without the surrounding <>"""
        result = []

        for pre, nam in graph.namespaces():
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            result.append(nam.n3()[1:-1])

        return result

    # TODO (@pedropaulofb): Crete function to verify if a class in an ontology is an instance of a GUFO class
    # TODO (@pedropaulofb): Crete function to verify if a class in an ontology is a subclass of a GUFO class
