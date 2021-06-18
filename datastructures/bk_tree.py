class Node:

    def __init__(self,payload):
        self._payload = payload
        self._children = {}
        
    @property
    def payload(self):
        return self._payload

    def add_child(self,child_node,metric_function):
        distance = metric_function(self._payload,child_node.payload)
        if distance not in self._children:
            self._children[distance] = child_node
        else:
            self._children[distance].add_child(child_node,metric_function)
    
    def search(self,search_term,tolerance,metric_function,results_list):
        distance = metric_function(self._payload,search_term)
        results_list.append((self._payload,distance))
        min_search_distance = distance - tolerance
        min_search_distance = min_search_distance if min_search_distance > 1 else 1
        max_search_distance = distance + tolerance

        for dist in self._children.keys():
            if dist >= min_search_distance and dist <= max_search_distance:
                self._children[dist].search(search_term,tolerance,metric_function)

        


class BKTree:

    def __init__(self,metric_function):
        self._root = None
        self._metric_function = metric_function

    def add_element(self,element):
        if self._root is None:
            self._root = Node(element)
        else:
            self._root.add_child(Node(element),self._metric_function)

    def search(self,search_term,tolerance,results_list=[]):
        if self._root is None:
            raise LookupError('BKTree has no children.')
        self._root.search(search_term,tolerance,self._metric_function,results_list)