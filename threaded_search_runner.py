from dataclasses import dataclass,field
from typing import Any

@dataclass(order=True)
class PriorityizedItem:
    priority: int
    item: Any=field(compare=False)

from threading import Thread
from datastructures.bk_tree import BKTree
from time import time_ns,sleep
from queue import PriorityQueue

class SearchRunner(Thread):
    
    def __init__(self,bktree:BKTree,search_term:str,pqueue:PriorityQueue,**kwargs):
        self._bktree = bktree
        self._search_term = search_term
        self._priority_queue = pqueue
        super().__init__(**kwargs)

    def run(self):
        time_started = time_ns()
        results = self._bktree.search(self._search_term,3,[])
        sleep(.1)
        #ensure that new results are pulled first
        self._priority_queue.put(PriorityizedItem(-1*time_started,results))

