from abc import ABC, abstractmethod
from datastructures.bk_tree import BKTree

class DictionaryResource(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self,bk_tree:BKTree):
        pass

    @abstractmethod
    def remove(self):
        pass

import os
import random
from datastructures.bk_tree import BKTreeThreaded
from edit_distance import levenshtein_distance
import pickle
import threading

class DictionaryFileResource(DictionaryResource):

    def __init__(self,filename:str):
        self._filename = filename

    def load(self):
        with open(self._filename,'rb') as pickle_file:
            return pickle.load(pickle_file)

    def save(self,bktree:BKTree):
        with open(self._filename,'wb') as picke_file:
            pickle.dump(bktree,picke_file)

    def remove(self):
        if os.path.exists(self._filename):
            os.remove(self._filename)

    @property
    def filename(self):
        return self._filename




class DictionaryLoader:

    def __init__(self,dictionary_dir:str="dictionaries",dictionary_file_ext:str='.pbk'):
        self._dictionary_dir = dictionary_dir
        #make sure dot is includes
        if dictionary_file_ext[0] != '.':
            dictionary_file_ext = '.' + dictionary_file_ext
        self._file_ext = dictionary_file_ext
        if not os.path.isdir(self._dictionary_dir):
            os.mkdir(self._dictionary_dir)
        
    
    def get_dictionary_list(self):
        contents = os.listdir(self._dictionary_dir)
        
        #only return dictionaries
        return [dictionary for dictionary in contents if dictionary[-len(self._file_ext):] == self._file_ext]

    def create_dictionary_builder(self,filepath:str):
        basename = os.path.basename(filepath).split('.')[0]
        with open(filepath,'r') as dict_text:
            words = dict_text.readlines()
        #prevent recursion issues with ordered lists
        dictionary_file_path = os.path.join(self._dictionary_dir,basename) + self._file_ext
        dictionary_resource = DictionaryFileResource(dictionary_file_path)
        return DictionaryBuilder(words,dictionary_resource,daemon=True)
    
    
    def load_dictionary(self,dictionary_file_name:str):
        dictionary_file_path = os.path.join(self._dictionary_dir,dictionary_file_name)
        return DictionaryFileResource(dictionary_file_path).load()

    @property
    def file_ext(self):
        return self._file_ext

from typing import Callable, List

class DictionaryBuilder(threading.Thread):

    def __init__(self,words:List[str],dictionary_resource:DictionaryResource,**kwargs):
        self._word_list = words
        self._dictionary_resource = dictionary_resource
        self._abort_lock = threading.Lock()
        self._progress_lock = threading.Lock()
        self._bktree_lock = threading.Lock()

        self._complete_listeners:List[Callable] = []


        self._abort_early = False
        self._progess = 0
        self._bktree = None
        super().__init__(**kwargs)

    def abort(self):
        with self._abort_lock:
            self._abort_early = True

    @property
    def progress(self):
        with self._progress_lock:
            return self._progress_lock

    @property
    def dictionary(self):
        with self._bktree_lock:
            return self._bktree

    def _build_tree(self,words):
        random.shuffle(words)
        dictionary = BKTreeThreaded(levenshtein_distance)
        total = len(words)
        for i in range(0,total):
            with self._abort_lock:
                if self._abort_early:
                    break
            dictionary.add_element(words[i])
            with self._progress_lock:
                self._progress = i/total
        return dictionary


    def run(self):
        with self._bktree_lock:
            self._bktree = self._build_tree(self._word_list)
        self._dictionary_resource.save(self._bktree)






    