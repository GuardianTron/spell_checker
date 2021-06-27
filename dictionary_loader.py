import os
import random
from datastructures.bk_tree import BKTreeThreaded
from edit_distance import levenshtein_distance
import pickle

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

    def create_dictionary(self,filepath:str):
        basename = os.path.basename(filepath).split('.')[0]
        with open(filepath,'r') as dict_text:
            words = dict_text.readlines()
        #prevent recursion issues with ordered lists
        random.shuffle(words)
        dictionary = BKTreeThreaded(levenshtein_distance,True)
        for word in words:
            dictionary.add_element(word.strip())
        
        dictionary_file_path = os.path.join(self._dictionary_dir,basename) + self._file_ext
        with open(dictionary_file_path,'wb') as pickle_file:
            pickle.dump(dictionary,pickle_file)
        return dictionary

    def load_dictionary(self,dictionary_file_name:str):
        dictionary_file_path = os.path.join(self._dictionary_dir,dictionary_file_name)
        with open(dictionary_file_path,'rb') as pickle_file:
            return pickle.load(pickle_file)






    