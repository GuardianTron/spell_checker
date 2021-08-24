import os
import random
from datastructures.bk_tree import BKTreeThreaded
from edit_distance import levenshtein_distance
import pickle
import threading


class DictionaryLoader:

    def __init__(self,dictionary_dir:str="dictionaries",dictionary_file_ext:str='.pbk'):
        self._dictionary_dir = dictionary_dir
        #make sure dot is includes
        if dictionary_file_ext[0] != '.':
            dictionary_file_ext = '.' + dictionary_file_ext
        self._file_ext = dictionary_file_ext
        if not os.path.isdir(self._dictionary_dir):
            os.mkdir(self._dictionary_dir)
        self._load_percentages = {}
        self._load_percentages_lock = threading.Lock()
        
        self._loaded_dictionaries_lock = threading.Lock()
        self._loaded_dictionaries = {}
    
    def get_dictionary_list(self):
        contents = os.listdir(self._dictionary_dir)
        
        #only return dictionaries
        return [dictionary for dictionary in contents if dictionary[-len(self._file_ext):] == self._file_ext]

    def create_dictionary(self,filepath:str):
        basename = os.path.basename(filepath).split('.')[0]
        with open(filepath,'r') as dict_text:
            words = dict_text.readlines()
        #prevent recursion issues with ordered lists
        random.shuffle(words)
        dictionary = self._build_tree(filepath,words)
        dictionary_file_path = os.path.join(self._dictionary_dir,basename) + self._file_ext
        with open(dictionary_file_path,'wb') as pickle_file:
            pickle.dump(dictionary,pickle_file)
        return dictionary

    def load_dictionary(self,dictionary_file_name:str):
        dictionary_file_path = os.path.join(self._dictionary_dir,dictionary_file_name)
        with open(dictionary_file_path,'rb') as pickle_file:
            return pickle.load(pickle_file)

    def _build_tree(self,filename,words):
        dictionary = BKTreeThreaded(levenshtein_distance)
        total = len(words)
        for i in range(0,total):
            dictionary.add_element(words[i])
            self._set_load_progress(i/total)
        return dictionary



    def _set_load_progress(self,filename,percent):
        with self._load_percentages_lock:
            self._load_percentages[filename] = percent

    def get_load_progress(self,filename):
        with self._load_percentages_lock:
            percentage = self._load_percentages[filename]
        return percentage
    
    def get_loaded_dictionary(self,filename):
        with self._loaded_dictionaries_lock:
            return self._loaded_dictionaries[filename]
    
    def _set_loaded_dictionary(self,filename,dictionary):
        with self._loaded_dictionaries_lock:
            self._loaded_dictionaries[filename] = dictionary

    @property
    def file_ext(self):
        return self._file_ext

from typing import List

class DictionaryBuilder(threading.Thread):

    def __init__(self,words:List[str],**kwargs):
        self._word_list = words
        self._abort_lock = threading.Lock()
        self._progress_lock = threading.Lock()
        self._bktree_lock = threading.Lock()


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

    def _build_tree(self,words):
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






    