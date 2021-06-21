from datastructures.bk_tree import BKTree
from edit_distance import levenshtein_distance
import random
import sys
import timeit
import pickle

'''
Developer: Anthony Feeney
Email: feeney.anthony.l@gmail.com

This script implements a basic spellchecker utilizing a
memory optimized version of Wagner-Fischer algorithm to 
calculate the edit distance for words and a BK Tree to 
limit comparisons. 
Lists up to 25 words that are the closest match to the 
supplied string.

Usage:
Pass string to be checked as parameter.
'''

def load_dictionary(filename='usa.txt'):
    '''
    Loads the dictionary from file and stores in BKTree

    This function will load dictionary database from a 
    pickled BK tree if found.
    If not found, a text file consisting of words separated by \\n 
    newline characters will loaded and and processed into a BK tree
    which will then be pickled.   

    Keyword arguments:
    filename --- Name of the text file containing the dictionary

    Return: BKTree
    '''
    with open('usa.txt','r') as words_file:
        words = words_file.readlines()
    random.shuffle(words)
    try:
        dictionary_handle = open('dictionary','rb')
        dictionary = pickle.load(dictionary_handle)
        dictionary_handle.close()
    except:
        dictionary = BKTree(levenshtein_distance)

        for word in words:
            dictionary.add_element(word.strip())
        dictionary_handle = open('dictionary','wb')
        pickle.dump(dictionary,dictionary_handle)
        dictionary_handle.close()
    return dictionary

if __name__ == "__main__":

    search_string = sys.argv[1].strip()
    dictionary = load_dictionary()
    results = dictionary.search(search_string,4)

    results.sort(key= lambda result_tuple: result_tuple[1])
    print(f'Search String: {search_string}')
    print(f'Number dictionary results: {len(results)}')
    print(f'{"-"*20}')
    num_results_to_display = min(25,len(results))
    for i in range(0,num_results_to_display):
        word,score = results[i]
        word = word.strip()
        print(f"{word:15}  {score} ")


