

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
        if distance <= tolerance:
            results_list.append((self._payload,distance))
        min_search_distance = distance - tolerance
        min_search_distance = min_search_distance if min_search_distance > 1 else 1
        max_search_distance = distance + tolerance

        for dist in self._children.keys():
            if dist >= min_search_distance and dist <= max_search_distance:
                self._children[dist].search(search_term,tolerance,metric_function,results_list)

from threading import Lock
class  NodeThreaded(Node):

    def __init__(self,payload,parent_tree):
        self._parent_tree = parent_tree
        self._insert_lock = Lock()
        super().__init__(payload)
    
    '''
        Search through the tree for matches within tolerance. If another thread
        changes the term being searched, the search will abort early.
    '''

    def search(self,search_term,tolerance,metric_function,results_list):
        #utilizes BKTreeTreaded.current_search's lock to handling locking
        if self._parent_tree.current_search and self._parent_tree.current_search == search_term:
            super().search(search_term,tolerance,metric_function,results_list)

    def add_child(self, child_node, metric_function):
        with self._insert_lock:
            super().add_child(child_node, metric_function)

    #Remove locks from pickling
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_insert_lock']
        return state
    
    def __setstate__(self,state):
        self.__dict__.update(state)
        self._insert_lock = Lock()
    


class BKTree:

    '''A Burkhard-Keller Tree implementation.'''

    def __init__(self,metric_function):
        '''Takes a metric function that wil be used to compare and store elements.'''
        self._root = None
        self._metric_function = metric_function

    def add_element(self,element):
        '''Adds an element to the tree.'''
        if self._root is None:
            self._root = self._new_node(element)
        else:
            self._root.add_child(self._new_node(element),self._metric_function)

    def search(self,search_term,tolerance,results_list=[]):
        '''Returns all items within the tree within a given tolerance to search_term.'''
        if self._root is None:
            raise LookupError('BKTree has no children.')
        self._root.search(search_term,tolerance,self._metric_function,results_list)
        return results_list

    '''
        Provides hook to allow subclasses to replace 
        the type of node created.
    '''
    def _new_node(self,element:str,*args,**kwargs) -> Node:
        return Node(element)



class BKTreeThreaded(BKTree):

    ''' A BK Tree implementation that allows for aborting expired searches early.'''

    def __init__(self,metric_function,preempt_search = True):
        self._search_term_lock = Lock()
        self._preempt_search = preempt_search
        self._current_search = None

        super().__init__(metric_function)

    def search(self,search_term,tolerance,results=[]):
        if self._preempt_search:
            with self._search_term_lock:
                self._current_search = search_term
        return super().search(search_term,tolerance,results)

    @property
    def current_search(self):
        with self._search_term_lock:
            return self._current_search

    def _new_node(self, element: str, *args, **kwargs) -> Node:
        return NodeThreaded(element,self)

    #Handle errors from pickling the lock objects
    def __getstate__(self):
       state = self.__dict__.copy()
       del state['_current_search']
       del state['_search_term_lock']
       return state

    def __setstate__(self,state):
        self.__dict__.update(state)
        self._current_search = None
        self._search_term_lock = Lock()