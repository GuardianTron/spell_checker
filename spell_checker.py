from datastructures.bk_tree import BKTreeThreaded
from datastructures.priority_queue_updatedable import PriorityQueueUpdateable
from interface_elements.spell_elements import ResultsWindow,InputWindow
from edit_distance import levenshtein_distance
from threading import Lock
import random
import sys
import curses
from curses import ascii
from threaded_search_runner import SearchRunner
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

def load_dictionary(filename=None):
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
    if filename is not None:
        return create_dictionary_from_file(filename)
    else:
        with open('dictionary.pbk','rb') as dict_file:
            return pickle.load(dict_file)

def create_dictionary_from_file(filename:str):
    with open(filename,'r') as word_file:
        words = word_file.readlines()
    #prevent recursion depth overflow
    random.shuffle(words)
    dictionary = BKTreeThreaded(levenshtein_distance)
    for word in words:
        dictionary.add_element(word.strip())
    with open('dictionary.pbk','wb') as dict_file:
        pickle.dump(dictionary,dict_file)
    return dictionary


def c_main(stdscr):
    stdscr.nodelay(1)
    word_window = InputWindow(0,0)
    #set up results window
    results_window_height = curses.LINES - 2
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    results_window = ResultsWindow(results_window_height,40,2,5,1)
    
    new_text_file_path = sys.argv[1] if len(sys.argv) > 1 else None
   
    dictionary = load_dictionary(new_text_file_path)

       
    word = ''
    results_pqueue = PriorityQueueUpdateable()
    threads = []
    while True:
        character = stdscr.getch()
        word_changed = False
        list_updated = False
        if curses.ascii.iscntrl(character):
            if character == curses.ascii.ESC:
                break
        word_window.process_input(character)
        if word != word_window.text:
            word = word_window.text
            word_changed = True
            
        #update spell check list if word has changed  
        if word_changed:
            search = SearchRunner(dictionary,word,results_pqueue,daemon=True)
            threads.append(search)
            search.start()
            #results = dictionary.search(word,3,[])  
            
                
        if results_pqueue.has_new_results():
            results = results_pqueue.get_latest_result()
            #sort by levenshtein distance then remove 
            results.sort(key=lambda results: results[1])
            results_window.results = [result[0] for result in results]
            results_window.draw()
            
            
        if list_updated or word_changed:
            word_window.draw()
        cursor_x = len(word) if len(word) < curses.COLS - 1 else curses.COLS - 1
        stdscr.move(0,cursor_x) 
    return 0

def main():
    try:
        return curses.wrapper(c_main)
    except FileNotFoundError:
        if len(sys.argv) > 1:
            print('The text file you attempted to upload could not be found.')
        else:
            print('The dictionary could not be found. Please select file to upload.')
if __name__ == "__main__":
    exit(main())


